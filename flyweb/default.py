from flyweb import Response

def defaultIndex(request):
    return Response('默认首页！')

def default404(request):
    return Response('页面不存在！', 404)

def defaultMethodErr(request):
    return Response('页面%s不能用%s方法请求！'%(request.path,request.method), 404)

def default401(request):
    return Response('非法请求', 401)

def default500(request):
    return Response('服务器发生错误', 500)

defaultURL = {'40x':defaultMethodErr, '404': default404, '401': default401, '500':default500}
staticDir = []
from flyweb import route
baseRoute = route.TreeRoute(defaultURL,staticDir)
