import os
import importlib
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request
from hasweb.route import base_route
from hasweb.default import appDir,ActionPrefix,ControllerDir,ControllerSuffix,ActionsMethod,defaultMethod, \
    userFilter,FilterDir,FilterSuffix,BeforeAction,AfterAction

def loadController():
    fun_prefix_lenght = len(ActionPrefix)
    file_suffix_lenght = len(ControllerSuffix)+3
    tag_dir = os.path.join(os.getcwd(),ControllerDir)
    for one_file in os.listdir(tag_dir): # 遍历处理目录下的文件
        if one_file.endswith('%s.py'%ControllerSuffix):
            use_filter = userFilter
            controller_name = one_file[0:-file_suffix_lenght]
            python_file_module = importlib.import_module('%s.%s%s' % (ControllerDir,controller_name, ControllerSuffix))
            controller_path = controller_name.lower()  # 路径统一用小写存储


            before_action_fun,after_action_fun = None,None
            for k in dir(python_file_module): #遍历提取过滤器
                if k == BeforeAction:
                    _action_fun = getattr(python_file_module, k)  # 获取模块(文件)中的函数
                    if callable(_action_fun):
                        before_action_fun = _action_fun
                if k == AfterAction:
                    _action_fun = getattr(python_file_module, k)  # 获取模块(文件)中的函数
                    if callable(_action_fun):
                        after_action_fun = _action_fun
                if k == 'useFilter':
                    use_filter = _action_fun = getattr(python_file_module, k)

            before_action_list = list()
            after_action_list = list()
            for temp_filter_name in use_filter:  # 配置在userFilter列表中的过滤器
                one_filter = base_route.tempFilter.get(temp_filter_name)
                if one_filter[0] != None:
                    before_action_list.append(one_filter[0])
                if one_filter[1] != None:
                    after_action_list.append(one_filter[1])
            if before_action_fun != None:
                before_action_list.append(before_action_fun)
            if after_action_fun != None:
                after_action_list.append(after_action_fun)


            actionsMethod = getattr(python_file_module, ActionsMethod, dict()) #获取文件中的method字典
            for k in dir(python_file_module):
                if k.startswith(ActionPrefix) and len(k) > fun_prefix_lenght:
                    fun = getattr(python_file_module, k)  # 获取模块(文件)中的函数
                    if callable(fun):
                        action_path = k[fun_prefix_lenght:].lower()
                        method = actionsMethod.get(action_path, defaultMethod)
                        #添加路由信息，路由信息:[路径字符串，请求方法，函数列表]
                        base_route.addRoute('%s/%s' % (controller_path, action_path), method, [before_action_list, fun, after_action_list])

def initFilter():
    file_suffix_lenght = len(FilterSuffix) + 3 #加3是因为.py 如："Filter.py"
    tag_dir = os.path.join(os.getcwd(), FilterDir)
    for one_file in os.listdir(tag_dir):  # 遍历处理目录下的文件
        if one_file.endswith('%s.py' % FilterSuffix):
            filter_name = one_file[0:-file_suffix_lenght]
            python_file_module = importlib.import_module('%s.%s%s' % (FilterDir, filter_name, FilterSuffix))
            _name = filter_name.lower()
            before_action_fun, after_action_fun = None, None
            for k in dir(python_file_module):  #处理所有过滤器
                if k == BeforeAction:
                    _action_fun = getattr(python_file_module, k)  # 获取模块(文件)中的函数
                    if callable(_action_fun):
                        before_action_fun = _action_fun
                if k == AfterAction:
                    _action_fun = getattr(python_file_module, k)  # 获取模块(文件)中的函数
                    if callable(_action_fun):
                        after_action_fun = _action_fun
            base_route.tempFilter[_name] = [before_action_fun, after_action_fun]

#添加路由
def initRoute():
    initFilter() #处理全局过滤器，下面的loadController用到这一步的处理结果
    loadController()


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
        os.chdir(appDir)
        web = Web()

        if use_debugger:
            print(base_route.mainURL)
            # print(base_route.tempFilter)

        run_simple(hostname, port, web, use_reloader,use_debugger,
                   use_evalex,extra_files,reloader_interval,reloader_type,
                   threaded,processes,request_handler,static_files,passthrough_errors,ssl_context)