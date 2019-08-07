import inspect
from hasweb.default import defaultURL,staticDir
from hasweb.render import dispatch_static

def getBasePath(path):
    return path.strip().strip('/')

#表示路由中的一段路径的节点
class RouteNode(object):
    def __init__(self,path=None,method={},fun=None):
        self.path = path  # 路径
        self.method = method
        self.fun = fun  # 函数，不一定存在
        self.children = []  # 子节点

    def __str__(self):
        if len(self.children) == 0:
            return "'%s'"%self.path
        return '"%s"=>[%s]'%(self.path,','.join(map(lambda n:str(n),self.children )))

#用树状结构存储路由信息
class TreeRoute(object):
    def __init__(self):
        self.mainURL = RouteNode() #根节点，不算进路径
    def __createNode(self,url_part, method, func):
        return RouteNode(url_part, method, func)

    #建立路由时查找,找不到时返回None
    def __findNodeForInsert(self,parent_node,url_part,method):
        tag_node = None
        for child in parent_node.children:
            if len(method) == len(child.method):
                ok = True
                for tag_method in child.method:
                    if tag_method not in method:
                        ok = False
                        break
                if ok == False:
                    continue
            else:
                continue
            #查找条件：节点中的字段相等
            if url_part == child.path:
                tag_node = child
                break
        return tag_node

    #解析路由时查找
    def __findNode(self,parent_node,url_part,method):
        tag_node = None
        for child in parent_node.children:
            #查找条件：节点中的字段相等或者节点类型被参数 且method符合
            if url_part == child.path and (len(child.method) ==0 or method in child.method):
                tag_node = child
                break
        return tag_node

    def __getResponse(self,url_path,method,request):
        # print(inspect.getargspec(fun)) ArgSpec(args=['request'], varargs=None, keywords=None, defaults=None)
        path_list = url_path.split('/')
        path_list_lenght = len(path_list)
        exist_node = self.mainURL
        i = 0
        print(path_list)
        while i < path_list_lenght:
            result_node = self.__findNode(exist_node, path_list[i],method)
            print('result_node', result_node)
            if result_node == None:
                break
            exist_node = result_node
            i = i + 1
        if i == path_list_lenght:
            print(exist_node)
            return exist_node.fun(request)

    # 添加路由对应的处理函数,已经存在的不会覆盖
    def addRoute(self, path_list, method, func):
        exist_node = self.mainURL
        i = 0
        while i<len(path_list):
            result_node = self.__findNodeForInsert(exist_node, path_list[i],method)
            if result_node == None:
                break
            exist_node = result_node
            i = i+1
        while i<len(path_list): #处理不存在的路由
            new_node = self.__createNode(path_list[i], method, func)
            exist_node.children.append(new_node)
            exist_node = new_node
            i = i+1


    # 根据请求的路径和方法获取处理函数
    def getResponse(self, request):
        url_path = getBasePath(request.path)
        method = request.method
        try:
            tag_response = self.__getResponse(url_path,method,request)
            if tag_response!=None:
                return tag_response

            # 最后考虑是静态资源的情况,不把处理静态资源作为优势
            if url_path.startswith(staticDir):
                return dispatch_static(url_path)
        except Exception as e:
            print(__name__, 'e.__str__():', e.__str__())
            return defaultURL['500'](request)
        return defaultURL['404'](request)

base_route = TreeRoute()