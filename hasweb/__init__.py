import os
import importlib
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request
from hasweb.route import base_route
from hasweb.default import appDir,action_prefix

#添加路由
def initRoute():
    pure_dir = appDir.lstrip('.').strip('/')
    controller_dir_module = importlib.import_module('%s.controller'%pure_dir) #加载controller(目录)模块
    _path  = controller_dir_module.__path__._path[0] #controller目录
    dirList = os.listdir(_path)
    prefix_lenght = len(action_prefix)
    #遍历处理controller目录下的文件
    for one_file in dirList:
        if one_file.endswith('.py'):
            controller_name = one_file[0:-3]
            python_file_module = importlib.import_module('hasDemo.controller.%s'%controller_name)
            controller_path = controller_name.lower() #路径统一用小写存储
            for k in dir(python_file_module):
                if k.startswith(action_prefix) and len(k)>prefix_lenght:
                    fun = getattr(python_file_module, k) #获取模块(文件)中的函数
                    if callable(fun):
                        action_path = k[prefix_lenght:].lower()
                        base_route.addRoute([controller_path,action_path], {}, fun)


class Web(object):
    def __init__(self, config={}):
        initRoute()

    def dispatch_request(self,request):
        response = base_route.getResponse(request)
        return response
        # return check_response(response, request)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


class WebService:
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

        web = Web()
        print(base_route.mainURL)
        run_simple(hostname, port, web, use_reloader,use_debugger,
                   use_evalex,extra_files,reloader_interval,reloader_type,
                   threaded,processes,request_handler,static_files,passthrough_errors,ssl_context)