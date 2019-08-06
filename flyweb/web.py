from werkzeug.serving import run_simple
import werkzeug.wrappers as wrappers
from flyweb.default import baseRoute
from flyweb.tool import check_response


class Flyweb(object):
    def __init__(self, baseRoute, config={}):
        # print('config',config)
        self.baseRoute = baseRoute

    def dispatch_request(self,request):
        response = self.baseRoute.getResponse(request)
        return check_response(response,request)

    def wsgi_app(self, environ, start_response):
        request = wrappers.Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

class Blueprint:
    def __init__(self, url_prefix,name):
        self.url_prefix = url_prefix
        self.arr = [] #
    # 路由装饰器
    def route(self, path, method={}):
        def decorator(func):
            self.arr.append([path,method,func])
        return decorator


class Hasfly:
    def __init__(self, name):
        # print('__name__',name)
        self.baseRoute = baseRoute

    #路由装饰器
    def route(self,path,method={}):
        def decorator(func):
            # 添加路由对应的处理函数
            self.baseRoute.addRoute(path,method,func)
            # def wrapper(*args, **kwargs):
            #     return func(*args, **kwargs)
            # wrapper.__name__ = func.__name__
        return decorator

    #错误页面装饰器
    def errorhandler(self,code):
        def decorator(func):
            # 添加响应编码对应的处理函数
            self.baseRoute.addDefaultRoute(code, func)
        return decorator

    # 批量添加带前缀的路由函数
    def register_blueprint(self,blueprint,url_prefix=None):
        #若url_prefix不为空，测用url_prefix替代blueprint.url_prefix
        the_prefix = blueprint.url_prefix if url_prefix==None else url_prefix
        self.baseRoute.addPrefixRoute(the_prefix,blueprint.arr)

    # 添加静态资源目录
    def addStatic(self,path):
        self.baseRoute.addStatic(path)

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
        print(self.baseRoute.mainURL)

        app = Flyweb(self.baseRoute)
        run_simple(hostname, port, app, use_reloader,use_debugger,
                   use_evalex,extra_files,reloader_interval,reloader_type,
                   threaded,processes,request_handler,static_files,passthrough_errors,ssl_context)