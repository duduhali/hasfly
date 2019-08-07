from enum import Enum,unique
from flyweb.render import dispatch_static
from flyweb.local_config import url_suffix

def getBasePath(path):
    return path.strip().strip('/')

def getPathList(path):
    return path.strip().strip('/').split('/')

#用字符串储路由信息
class BaseRoute(object):
    # 添加路由对应的处理函数, 需要由子类实现
    def addRoute(self, path, method, func):
        pass

    # 批量添加带前缀的路由函数
    def addPrefixRoute(self, url_prefix, arr):
        prefix = getBasePath(url_prefix)  # 前缀
        for path, method, func in arr:
            self.addRoute('%s/%s' % (prefix, getBasePath(path)), method, func)

    # 添加响应编码对应的处理函数
    def addDefaultRoute(self, code, func):
        self.defaultURL[repr(code)] = func

    # 添加静态资源目录
    def addStatic(self, path):
        self.staticDir.append(getBasePath(path))

    # 根据请求的路径和方法获取处理函数, 需要由子类实现
    def getResponse(self, request):
        pass

#表示路由节点的类型
@unique
class NodeType( Enum ):
    View = 0   #路径
    Param = 1   #路径中的参数，如：<name>
#表示路由中的一段路径的节点
class RouteNode(object):
    def __init__(self, node_type,path,method,fun):
        self.node_type = node_type  # 节点类型
        self.path = path  # 路径
        self.method = method
        self.fun = fun  # 函数，不一定存在
        self.children = []  # 子节点

    def __str__(self):
        if len(self.children) == 0:
            return "'%s'"%self.path
        return '"%s"=>[%s]'%(self.path,','.join(map(lambda n:str(n),self.children )))

#用树状结构存储路由信息
class TreeRoute(BaseRoute):
    def __init__(self,defaultURL,staticDir):
        self.mainURL = RouteNode(None,None,None,None) #根节点，不算进路径
        self.defaultURL = defaultURL
        self.staticDir = staticDir
    def __createNode(self,url_part, method, func):
        if url_part.startswith('<') and url_part.endswith('>'):
            node_type = NodeType.Param
        else:
            node_type = NodeType.View
        return RouteNode(node_type, url_part, method, func)
    #从传入节点的子节点中查找符合条件的节点
    def __findNodeForInsert(self,parent_node,url_part,method):
        tag_node = None
        for one_node in parent_node.children:
            if len(method) == len(one_node.method):
                ok = True
                for tag_method in one_node.method:
                    if tag_method not in method:
                        ok = False
                if ok == False:
                    continue
            else:
                continue
            #查找条件：节点中的字段相等或者节点类型被参数
            if one_node.node_type == NodeType.Param or url_part == one_node.path:
                tag_node = one_node
                break
        return tag_node
    def __findNode(self,parent_node,url_part,method):
        tag_node = None
        for one_node in parent_node.children:
            #查找条件：节点中的字段相等或者节点类型被参数 且method符合
            if (one_node.node_type == NodeType.Param or url_part == one_node.path) and \
                (len(one_node.method) ==0 or method in one_node.method):
                tag_node = one_node
                break
        return tag_node

    def __getResponse(self,path_list,method,request):
        path_list_lenght = len(path_list)
        exist_node = self.mainURL
        i = 0
        param_dict = dict()
        while i < path_list_lenght:
            result_node = self.__findNode(exist_node, path_list[i],method)
            if result_node == None:
                break
            exist_node = result_node
            if exist_node.node_type == NodeType.Param: #把路由中的参数保存到字典param_dict
                name_and_type = exist_node.path[1:-1].split(':')
                if len(name_and_type) == 1:
                    param_dict[name_and_type[0]] = path_list[i]
                else:
                    if name_and_type[1] == 'int':
                        param_dict[name_and_type[0]] = int(path_list[i])
                    elif name_and_type[1] == 'float':
                        param_dict[name_and_type[0]] = float(path_list[i])
            i = i + 1
        if i == path_list_lenght and exist_node != NodeType:
            # 查找的目标node
            if exist_node.node_type == NodeType.View:
                return exist_node.fun(request)
            elif exist_node.node_type == NodeType.Param:
                return exist_node.fun(request,**param_dict)

    # 重载方法，添加路由对应的处理函数,已经存在的不会覆盖
    def addRoute(self, path, method, func):
        path_list = getPathList(path)
        exist_node = self.mainURL
        i = 0
        while i<len(path_list):
            result_node = self.__findNodeForInsert(exist_node, path_list[i],method)
            if result_node == None:
                break
            exist_node = result_node
            i = i+1
        while i<len(path_list): #处理不存在的路由，已经存在的路径不执行这里的代码
            new_node = self.__createNode(path_list[i], method, func)
            exist_node.children.append(new_node)
            exist_node = new_node
            i = i+1


    # 重载方法，根据请求的路径和方法获取处理函数
    def getResponse(self, request):
        url_path = getBasePath(request.path)
        url_path = url_path.strip(url_suffix)  # 去掉路由的扩展名，如 /user/2.html=>/user/2
        method = request.method
        try:
            path_list = url_path.split('/')
            tag_response = self.__getResponse(path_list,method,request)
            if tag_response!=None:
                return tag_response

            if len(self.staticDir) != 0:  # 最后考虑是静态资源的情况,不把静态资源处理作为优势s
                for onePath in self.staticDir:
                    # 根据开头的字母，判断是不是请求的静态资源
                    if url_path.startswith(onePath):
                        return dispatch_static(url_path)
        except Exception as e:
            print(__name__, 'e.__str__():', e.__str__())
            return self.defaultURL['500'](request)
        return self.defaultURL['404'](request)

