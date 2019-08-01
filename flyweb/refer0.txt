#-*- coding:utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    '''处理请求并返回页面'''

    # 页面模板
    Page = '''\
        <html>
        <body>
        <p>Hello, web!</p>
        </body>
        </html>
    '''


    # 处理一个GET请求
    def do_GET(self):
        # print(dir(self))
        #实例变量
        # print(self.client_address)   #('127.0.0.1', 57239) 包括一个关于client地址的结构为 (host, port) 的元祖
        # print(self.server) #server实例   HTTPServer
        # print(self.command) #GET   包括命令(请求类型)，样例：'GET'
        # print(self.path) #默认 /   请求路径
        # print(self.request_version) #HTTP/1.1  请求的HTTP版本号的字符串，响应的头信息中没有
        # print(self.default_request_version) # HTTP/0.9  响应的头信息中没有HTTP/0.9
        # print(self.headers) #HTTP 请求的头信息
        # print(self.rfile) #一个输入流 stream，放置在输入数据选项的開始
        # wfile 输出流用于回复一个响应response给clientclient。当写入这些stream时必须使用适当的HTTP协议。

        # 有下列类变量
        # print(self.server_version) #BaseHTTP/0.6   指定服务器版本号。你或许会覆写它
        # print(self.sys_version) #Python/3.6.5     响应头信息里有 Server: BaseHTTP/0.6 Python/3.6.5
        # print(type(self.error_message_format),self.error_message_format) #错误界面字符串，用于创建一个错误响应给client
        # print(self.error_content_type) #指定错误响应的 Content-Type HTTP 头发送给client，缺省值是 'text/html;charset=utf-8'
        # print(self.protocol_version) #HTTP/1.0  响应中有 HTTP/1.0 200 OK   这个指定的HTTP协议版本号用于响应
        # 不管怎样，你的服务器必须包括一个精确的 Content-Length 头（使用 send_header()）在全部它响应的client中。为了向后兼容，默认设置为 'HTTP/1.0'。
        # print(self.MessageClass) #指定一个 rfc822.Message-like 类来解析HTTP头。典型的，这不用覆写，缺省设置 mimetools.Message
        # print(self.responses) #此变量包括一个错误码数字和一个包括短和长信息的2元祖的映射

        #实例有下面方法
        # handle()# 召唤一次handle_one_request() （或者。假设硬连接是启用的，多次召唤）来响应来到的HTTP请求。你应该永远不须要覆写它；反而。实现适当的do_ * 方法。
        # handle_one_request()#这种方法将解析和分配请求给适配do_ * 方法，你应该不须要覆写它。
        #send_error(code[, message]) #发送和记录一个完整的错误回复给client。code 指定HTTP错误码，message 是可选的， 很多其它特定文本。
        # send_response(code[,message]) 发送一个响应头和记录接受的请求，HTTP响应行被发送，然后是 Server 和 Data 头，这两个头的值分别从 version_string 和 dare_time_string 方法拾起
        #send_header(keyword, value) 向输出流写入一个指定的HTTP头，ketword 应该指定头关键字，value 指定它的值。
        #end_headers() 发送一个空白行，表面HTTP头响应结束。
        #log_request([code[,size]]) 记录和接受(成功的)请求，code 应该指定为 HTTP code 和响应通讯，假设响应大小是有效的。应该作为 size 參数。
        #log_error(…) 当一个请求不能被履行记录一个错误，缺省， 它把信息传给 log_message()，所以它获得相同的參数(格式的和附加的值)。
        #log_message(format, …)
        #记录一个随意的信息给 sys.tederr。这是典型的覆写来创建定制错误信息的原理。format參数是一个标准的 printf-style 格式化字符串，在其它參数 log_message() 被用作输入的格式。clientip地址和当前日期和时间作为每个信息记录(message logged)的前缀。
        # self.log_message('ssss')  #127.0.0.1 - - [31/Jul/2019 16:32:45] ssss


        # print(self.version_string()) #BaseHTTP/0.6 Python/3.6.5  返回服务器软件版本号。这是一个 server_version 和 sys_version 类变量的组合,头信息中的Server字段
        # print(self.date_time_string()) # Wed, 31 Jul 2019 08:47:23 GMT 返回由 timestramp 给予的日期和时间，通过一个信息头来格式化，假设 timestamp 被省略。它将使用当前的日期和时间
        # print(self.log_date_time_string()) #31/Jul/2019 17:44:20  #返回当前日期和时间。logging格式。
        # self.log_message(self.address_string())  #127.0.0.1 - - [31/Jul/2019 16:37:07] 127.0.0.1   返回client地址。logging格式。


        # print(self.close_connection) #True
        # print(self.connection)#<socket.socket fd=724, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8080), raddr=('127.0.0.1', 57611)>
        # print(self.request)  # <socket.socket fd=416, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8080), raddr=('127.0.0.1', 61978)>
        # print(self.default_request_version) # HTTP/0.9  响应的头信息中没有HTTP/0.9
        # print(self.disable_nagle_algorithm) #False  不知道什么意思
        # self.finish() 调用了之后会出错
        # self.flush_headers()  #调用了没发现变化
        # print(self.raw_requestline) #b'GET / HTTP/1.1\r\n'
        # print(self.requestline) #GET / HTTP/1.1   请求头信息中有这行
        # self.send_response_only(400)
        # print(self.timeout) #None
        # print(self.weekdayname) #['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(self.Page)))
        self.end_headers()
        self.wfile.write(self.Page.encode('utf-8'))

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        pass
        # mpath, margs = urllib.splitquery(self.path)
        # datas = self.rfile.read(int(self.headers['content-length']))
        # self.do_action(mpath, datas)
        #
        # def do_action(self, path, args):
        #     self.outputtxt(path + args)
        #
        # def outputtxt(self, content):
        #
        # # 指定返回编码
        # enc = "UTF-8"
        # content = content.encode(enc)
        # f = io.BytesIO()
        # f.write(content)
        # f.seek(0)
        # self.send_response(200)
        # self.send_header("Content-type", "text/html; charset=%s" % enc)
        # self.send_header("Content-Length", str(len(content)))
        # self.end_headers()
        # shutil.copyfileobj(f, self.wfile)

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    # server = ThreadedHTTPServer(('localhost', 8080), Handler)
    server.serve_forever()

