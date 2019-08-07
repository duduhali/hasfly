from werkzeug.wrappers import Response

appDir = '../hasDemo'          #项目目录,相对于run文件
defaultController = 'main'  #默认控制器
defaultAction = 'index'     #控制器的默认动作
staticDir = 'static'        #静态资源路径



action_prefix = 'action'    #动作的前缀，不建议修改




def default404(request):
    return Response('页面不存在！', 404)

def default401(request):
    return Response('非法请求', 401)

def default500(request):
    return Response('服务器发生错误', 500)

defaultURL = {'404': default404, '401': default401, '500':default500}

