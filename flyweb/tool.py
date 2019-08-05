import base64
import time
from flyweb import Response
import werkzeug.wrappers as wrappers
from flyweb.local_config import session_id

# 创建 Session ID
def create_session_id():
    # 首先获取当前时间戳，转换为字符串，编码为字节流，在 Base64 编码，在解码为字符串，然后去掉 Base64 编码会出现的“=”号，取到倒数第二位，最后再进行倒序排列
    return base64.encodebytes(str(time.time()).encode()).decode().replace("=", '')[:-2][::-1]

#检测和过滤返回内容
def check_response(response,request):
    if isinstance(response, wrappers.Response) == False:  # 返回的response 可能是字符串
        response = Response(str(response))

    # 处理cookie，如果键不在 cookies 中，则通知客户端设置 Cookie
    if session_id not in request.cookies:
        response.set_cookie(session_id, create_session_id())
    return response
    return response
