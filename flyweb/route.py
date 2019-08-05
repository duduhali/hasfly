from flyweb.render import dispatch_static
from flyweb.local_config import url_suffix

def getBasePath(path):
    return path.strip().strip('/')

#用字符串储路由信息
class BaseRoute(object):
    def __init__(self, mainURL,defaultURL,staticDir):
        self.mainURL = mainURL
        self.defaultURL = defaultURL
        self.staticDir = staticDir

    # 添加路由对应的处理函数
    def addRoute(self, path, method, func):
        self.mainURL[getBasePath(path)] = [func, method]

    # 批量添加带前缀的路由函数
    def addPrefixRoute(self, url_prefix, arr):
        prefix = getBasePath(url_prefix) # 前缀
        for path, method, func in arr:
            self.addRoute('%s/%s' % (prefix, getBasePath(path)), method, func)

    # 添加响应编码对应的处理函数
    def addDefaultRoute(self, code, func):
        self.defaultURL[repr(code)] = func

    # 添加静态资源目录
    def addStatic(self, path):
        self.staticDir.append(getBasePath(path))

    # 根据请求的路径和方法获取处理函数
    def getResponse(self, request):
        url_path = getBasePath(request.path)
        url_path = url_path.strip(url_suffix) #去掉路由的扩展名，如 /user/2.html=>/user/2
        method = request.method
        try:
            url_list = url_path.split('/')
            url_list_lenght = len(url_list)
            for one in self.mainURL.keys():
                one_list = one.split('/')
                i = 0
                parm_dict = dict()
                tag_url_list = []
                while len(one_list)>i and i<url_list_lenght:
                    item = one_list[i]
                    tag_url_list.append(item)
                    if item != url_list[i]:
                        if item.startswith('<') and item.endswith('>'):
                            name_and_type = item[1:-1].split(':')
                            if len(name_and_type)==1:
                                parm_dict[name_and_type[0]] = url_list[i]
                            else:
                                the_type = name_and_type[1]
                                the_data = url_list[i]
                                if the_type == 'int':
                                    the_data = int(the_data)
                                elif the_type == 'float':
                                    the_data = float(the_data)
                                parm_dict[name_and_type[0]] = the_data
                        else:
                            break
                    i = i+1
                if i==url_list_lenght:
                    tag_fun,methods = self.mainURL.get('/'.join(tag_url_list))
                    if len(methods) == 0 or method in methods:
                        if len(parm_dict)>0:
                            return tag_fun(request,**parm_dict)
                        else:
                            return tag_fun(request) #路径中不包含参数
                    return self.defaultURL['40x'](request)  # 路径正确，method有错

            #直接比较字符串，无法处理包含参数的路径，如：hi/<username>
            # tag_data = self.mainURL.get(url_path, None)
            # if tag_data != None:
            #     tag_fun, methods = tag_data
            #     if len(methods) == 0 or method in methods:
            #         return tag_fun(request)
            #     return self.defaultURL['40x'](request)  # 路径正确，method有错
            # else:
            #     return self.defaultURL['404'](request)

            if len(self.staticDir) != 0:  # 最后考虑是静态资源的情况
                for onePath in self.staticDir:
                    # 根据开头的字母，判断是不是请求的静态资源
                    if url_path.startswith(onePath):
                        return dispatch_static(url_path)
        except Exception as e:
            print(__name__, 'e.__str__():', e.__str__())
            return self.defaultURL['500'](request)
        return self.defaultURL['404'](request)
#用树状结构存储路由信息
class TreeRoute(BaseRoute):
    # 添加路由对应的处理函数
    def addRoute(self, path, method, func):
        pass

    # 批量添加带前缀的路由函数
    def addPrefixRoute(self, url_prefix, arr):
        pass

    # 添加静态资源目录
    def addStatic(self, path):
        pass

    # 根据请求的路径和方法获取处理函数
    def getResponse(self, request):
        pass

