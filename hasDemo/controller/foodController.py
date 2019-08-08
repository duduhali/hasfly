from werkzeug.wrappers import Response


useFilter = ['main'] #过滤器，若存在，本控制器中会用此属性替代全局配置

#beforeAction在filter之后，afterAction在filter之前
#返回False时不执行action,并转向错误页面
def beforeAction(request):
    print('one  beforeAction')
    # return False
#返回response
def afterAction(request,response):
    print('one  afterAction')
    return response

#默认配置文件中的defaultAction列表定义的方式
actionsMethod = {
    'index':['GET'],
    'hello':['GET','POST']
}

def actionIndex(request):
    # print('Index')
    return Response("Index")

def actionHello(request):
    # x = 1
    # print('Hello')
    return Response("hello")