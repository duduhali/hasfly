from werkzeug.wrappers import Response
import os
from hasweb.default import appDir

# 定义文件类型
TYPE_MAP = {
    'css':  'text/css',
    'js': 'text/js',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg'
}
#
def dispatch_static(static_file):
    # 判断资源文件是否在静态资源规则中，如果不存在，返回 404 状态页
    file = os.path.join(appDir,static_file)
    if os.path.exists(file):
        key = static_file.split(".")[-1] # 获取资源文件后缀
        doc_type = TYPE_MAP.get(key, 'text/plain') # 获取文件类型
        with open(file, 'rb') as f:
            data = f.read()
        return Response(data, content_type=doc_type)  # 封装并返回响应体
    else:
        return Response('静态资源不存在！', 404)