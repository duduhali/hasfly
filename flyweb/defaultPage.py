from flyweb import Response

def defaultIndex(request):
    return Response('默认首页！')

def default404(request):
    return Response('页面不存在！', 404)

def defaultMethodErr(request):
    return Response('页面%s不能用%s方法请求！'%(request.path,request.method), 404)

def default401(request):
    return Response('非法请求', 401)