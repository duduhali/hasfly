from werkzeug.serving import run_simple
from werkzeug.wrappers import Response

class FLYWEB:

    # 实例化方法
    def __init__(self, static_folder='static',template_folder='template', session_path=".session"):
        self.host = '127.0.0.1'  # 默认主机
        self.port = 8080  # 默认端口
        self.url_map = {}  # 存放 URL 与 Endpoint(节点名) 的映射
        self.static_map = {}  # 存放 URL 与 静态资源的映射
        self.function_map = {}  # 存放 Endpoint 与请求处理函数的映射

    def dispatch_request(self, request):
        # 定义 200 状态码表示成功
        # 返回响应体
        return Response('hello')

    # 启动入口
    def run(self, host=None, port=None, **options):
        # 如果 host 不为 None，替换 self.host
        if host:
            self.host = host
        # 如果 port 不为 None，替换 self.port
        if port:
            self.port = port
        # 把框架本身也就是应用本身和其它几个配置参数传给 werkzeug 的 run_simple
        run_simple(hostname=self.host, port=self.port, application=self, **options)

    # 框架被 WSGI 调用入口的方法
    def __call__(self, environ, start_response):
        return wsgi_app(self, environ, start_response)