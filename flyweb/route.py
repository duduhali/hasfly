from flyweb.default import defaultIndex,default404,defaultMethodErr,default401
from flyweb.render import dispatch_static


#转换路径，'/'=>'/'; '/xxxx'=>'/xxxx/'; '/xxxx/'=>'/xxxx/'
def getPath(path):
    tag_path = '/'+path.lstrip('/')
    tag_path = tag_path.rstrip('/')+'/'
    return tag_path


class BaseRoute(object):
    def __init__(self):
        self.urlMap = {'/': [defaultIndex, {}]}
        self.defaultURL = {'404': default404, '401': default401}
        self.staticDir = []

    #添加路由对应的处理函数
    def addRoute(self,path, method, func):
        pass

    # 批量添加带前缀的路由函数
    def addPrefixRoute(self,url_prefix,arr):
        pass

    # 添加响应编码对应的处理函数
    def addDeaultRoute(self,code, func):
        pass

    # 添加静态资源目录
    def addStatic(self, path):
        pass

    #根据请求的路径和方法获取处理函数
    def getResponse(self,request):
        pass

class StrRoute(BaseRoute):
    def addRoute(self,path, method, func):
        self.urlMap[getPath(path.strip(' '))] = [func, method]

    def addPrefixRoute(self,url_prefix,arr):
        prefix = url_prefix.strip(' ').strip('/')  # 前缀
        for path,method,func in arr:
            path_list = path.strip(' ').strip('/').split('/')
            tag_path = '%s/%s'%(prefix,'/'.join(path_list))
            self.urlMap[getPath(tag_path)] = [func, method]

    def addDeaultRoute(self,code, func):
        self.defaultURL[repr(code)] = func

    def addStatic(self, path):
        self.staticDir.append('/' + path.strip(' ').strip('/'))

    def getResponse(self, request):
        #先考虑是静态资源的情况
        url_path = request.path
        if len(self.staticDir) != 0:
            for onePath in self.staticDir:
                # 根据开头的字母，判断是不是请求的静态资源
                if url_path.startswith(onePath):
                    return dispatch_static(url_path)

        method = request.method
        client_path = getPath(request.path)
        try:
            path = self.urlMap.get(client_path, None)
            if path != None:
                path = self.urlMap[client_path]
                methods = path[1]
                if len(methods) == 0 or method in methods:
                    return path[0](request)
                return defaultMethodErr(request) #路径正确，method有错
            else:
                print("self.defaultURL['404']",client_path)
                return self.defaultURL['404'](request)
        except Exception as e:
            print(__name__,'e.__str__():',e.__str__())
        return self.defaultURL['401'](request)


