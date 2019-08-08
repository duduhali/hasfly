
def beforeAction(request):
    print('all  beforeAction')
    # return False
#返回response
def afterAction(request,response):
    print('all  afterAction')
    return response