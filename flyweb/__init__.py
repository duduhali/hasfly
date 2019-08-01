from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from flyweb.defaultPage import defaultIndex,default404,defaultMethodErr,default401

#转换路径，'/'=>'/'; '/xxxx'=>'/xxxx/'; '/xxxx/'=>'/xxxx/'
def getPath(path):
    tag_path = '/'+path.lstrip('/')
    tag_path = tag_path.rstrip('/')+'/'
    return tag_path

class Flyweb(object):
    def __init__(self, urlMap={},defaultURL={},config={}):
        # print('config',config)
        self.urlMap = urlMap
        self.defaultURL = defaultURL

    def dispatch_request(self,request):
        client_path = getPath(request.path)
        try:
            path = self.urlMap.get(client_path,None)
            if path != None:
                path = self.urlMap[client_path]
                methods = path[1]
                if len(methods) == 0 or request.method in methods:
                    return path[0](request)
                return defaultMethodErr(request)
            else:
                print(client_path)
                return self.defaultURL['404'](request)
        except Exception as e:
            print(e.__str__())
        return self.defaultURL['401'](request)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        if type(response) != Response:#返回的response 可能是字符串
            response = Response(response)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

class Blueprint:
    def __init__(self, prefix,name):
        self.prefix = prefix.strip(' ').strip('/') #路径
        self.urlMap = {}
    # 路由装饰器
    def route(self, path, method={}):
        def decorator(func):
            path_list = [self.prefix.strip(' ').strip('/')]
            path_list.extend(path.strip(' ').strip('/').split('/'))
            tag_path = '/'.join(path_list).strip('/')
            self.urlMap[getPath(tag_path)] = [func, method]
        return decorator


class Hasfly:
    def __init__(self, name):
        # print('__name__',name)
        self.urlMap = {'/': [defaultIndex,{}]}
        self.defaultURL = {'404': default404,'401': default401}

    #路由装饰器
    def route(self,path,method={}):
        def decorator(func):
            self.urlMap[getPath(path.strip(' '))] = [func, method]
            # def wrapper(*args, **kwargs):
            #     return func(*args, **kwargs)
            # wrapper.__name__ = func.__name__
        return decorator

    #错误页面装饰器
    def errorhandler(self,code):
        def decorator(func):
            self.defaultURL[repr(code)] = func
        return decorator

    def register_blueprint(self,blueprint):
        self.urlMap.update(blueprint.urlMap)

    def run(self,
            hostname,               #绑定的地址
            port,                   #端口
            use_reloader=False,     #是否自动加载，若为True则在有改动时自动加载
            use_debugger=False,
            use_evalex=True,
            extra_files=None,
            reloader_interval=1,
            reloader_type="auto",
            threaded=False,
            processes=1,
            request_handler=None,
            static_files=None,
            passthrough_errors=False,
            ssl_context=None,
            ):
        print(self.urlMap)

        app = Flyweb(urlMap=self.urlMap, defaultURL=self.defaultURL, config={})
        run_simple(hostname, port, app, use_reloader,use_debugger,
                   use_evalex,extra_files,reloader_interval,reloader_type,
                   threaded,processes,request_handler,static_files,passthrough_errors,ssl_context)