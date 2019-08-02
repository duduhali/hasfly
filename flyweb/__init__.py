import werkzeug.wrappers as wrappers

header_server = 'Hasfly Web 0.1'
#定制的Response
def Response(data,status=200,content_type='text/html',headers = {'Server': header_server}):
    # 返回响应体
    return wrappers.Response(data, content_type='%s; charset=UTF-8' % content_type, headers=headers, status=status)

def Header(data):
    headers = {'Server': header_server}
    headers.update(data)
    return headers


