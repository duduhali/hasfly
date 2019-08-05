import json
import os
from flyweb import Response,Header
from flytemplate import Templite
from flyweb.local_config import templite_extensions,templite_path

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
    file = static_file.lstrip('/')
    if os.path.exists(file):
        key = static_file.split(".")[-1] # 获取资源文件后缀
        doc_type = TYPE_MAP.get(key, 'text/plain') # 获取文件类型
        with open(file, 'rb') as f:
            data = f.read()
        return Response(data, content_type=doc_type)  # 封装并返回响应体
    else:
        return Response('静态资源不存在！', 404)

# 封装 JSON 数据响应包
def render_json(data):
    content_type = "text/plain"  # 定义默认文件类型为纯文本
    # 如果是 Dict 或者 List 类型，则开始转换为 JSON 格式数据
    if isinstance(data, dict) or isinstance(data, list):
        data = json.dumps(data)  # 将 data 转换为 JSON 数据格式
        content_type = "application/json"  # 定义文件类型为 JSON 格式
    return Response(data, content_type=content_type)

# URL 重定向方法
def redirect(url, status_code=302):
    response = Response('', status=status_code)
    # 为响应体的报头中的 Location 参数与 URL 进行绑定 ，通知客户端自动跳转
    response.headers['Location'] = url
    return response


# 模版引擎接口
def render_template(path, **kwargs):
    # 判断服务器是否有该文件，没有则返回 404 错误
    temp_path = '%s%s.%s'%(templite_path,path,templite_extensions)
    templite_path
    if os.path.exists(temp_path):
        with open(temp_path, "r", encoding='utf-8') as f:
            content = f.read()
        templite = Templite(content, kwargs)
        return Response(templite.render())
    # 如果不存在该文件，返回 404 错误
    return Response('模板文件不存在！', 404)


# 返回让客户端保存文件到本地的响应体
def render_file(file_path, file_name=None):
    # 判断服务器是否有该文件，没有则返回 404 错误
    if os.path.exists(file_path):
        # 判断是否有读取权限，没有则抛出权限不足异常
        # if not os.access(file_path, os.R_OK):
        #     raise exceptions.RequireReadPermissionError

        with open(file_path, "rb") as f:
            content = f.read()
        if file_name is None:  # 如果没有设置文件名，则以 “/” 分割路径取最后一项最为文件名
            file_name = file_path.split("/")[-1]
        # 封装响应报头，指定为附件类型，并定义下载的文件名
        headers = Header({ 'Content-Disposition': 'attachment; filename="%s"' % file_name})
        return Response(content, headers=headers)
    # 如果不存在该文件，返回 404 错误
    return Response('下载的文件不存在！', 404)