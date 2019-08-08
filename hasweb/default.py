from werkzeug.wrappers import Response

#以后移到工程目录
appDir = '../hasDemo'          #项目目录,相对于run文件
defaultController = 'main'  #默认控制器 ,
# 默认控制器的默认动作是首页，访问默认控制器的其它动作时不能省略控制器名，这样会认为是其它控制器的默认动作

staticDir = 'static'        #静态资源路径

userFilter = ['main','two']   #过滤器，添加顺序决定调用顺序
defaultMethod = [] #默认请求方式，空列表代表允许所有类型的请求,格式:['GET','POST']

#留在框架目录
# 不建议修改的配置
ControllerDir = 'controller' #控制器目录
ControllerSuffix = 'Controller' #控制器文件后缀

FilterDir = 'filter'        #过滤器目录
FilterSuffix = 'Filter' #过滤器文件后缀
BeforeAction = 'beforeAction' #前置过滤
AfterAction = 'afterAction' #后置过滤

DefaultAction = 'index'     #控制器的默认动作
ActionPrefix = 'action'    #动作的前缀

ActionsMethod = 'actionsMethod' #控制器中定义method的属性




def default404(request):
    return Response('页面不存在！', 404)

def default500(request):
    return Response('服务器发生错误', 500)

defaultURL = {'404': default404, '500':default500}

