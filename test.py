from flyweb import Hasfly
from flyweb import Response
# from admin import admin

app = Hasfly(__name__)
# app.register_blueprint(admin)

@app.route('/',method={'GET','POST'})
def index(request):
    # print(request.path)
    # print(request.method)
    # print(request.remote_addr)
    return Response('首页 Hi')

@app.route('/hi/<username>')
def hi(request,username):
    return Response('Hi')

@app.errorhandler(404)
def page_not_found(request):
    return Response('我是404错误')

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, use_debugger=True, use_reloader=False)

