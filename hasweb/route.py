import inspect
from hasweb.default import defaultURL,staticDir
from hasweb.render import dispatch_static

class Route(object):
    def __init__(self):
        self.mainURL = dict()
        self.tempFilter = dict()

    #添加路由，路由只有控制器和动作两层
    #func_list: [before_action_fun,fun,after_action_fun]
    def addRoute(self, path, method, func_list):
        self.mainURL[path] = [method, func_list]


    def filter(self,request,func_list):
        for before in func_list[0]:
            if before(request) == False:
                return

        response = func_list[1](request)

        for after in func_list[2][::-1]:
            response = after(request,response)

        return response

    # 根据请求的路径和方法获取处理函数
    def getResponse(self, request):
        url_path = request.path.strip('/')
        node = self.mainURL.get(url_path,None)
        if node != None:
            tag_method = node[0]
            if len(tag_method)==0 or request.method in tag_method:
                func_list = node[1]
                try:
                    result = self.filter(request,func_list)
                    if result !=None:
                        return result
                    ##############################################
                except Exception as e:
                    print(__name__, 'e.__str__():', e.__str__())
                    return defaultURL['500'](request)

        # 最后考虑是静态资源的情况,不把处理静态资源作为优势
        if url_path.startswith(staticDir):
            return dispatch_static(url_path)

        return defaultURL['404'](request)

base_route = Route()