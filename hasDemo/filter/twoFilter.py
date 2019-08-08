
def beforeAction(request):
    print('all2  beforeAction')
    # return False
#返回response
def afterAction(request,response):
    print('all2  afterAction')
    return response