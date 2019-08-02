import base64
import time

# 创建 Session ID
def create_session_id():
    # 首先获取当前时间戳，转换为字符串，编码为字节流，在 Base64 编码，在解码为字符串，然后去掉 Base64 编码会出现的“=”号，取到倒数第二位，最后再进行倒序排列
    return base64.encodebytes(str(time.time()).encode()).decode().replace("=", '')[:-2][::-1]

def check_response(response):

    return response
