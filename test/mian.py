from flyweb.web import Hasfly
from flyweb.render import *
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
def hi(request):
    return 'Hi'

@app.route('temp')
def hi(request):
    products = [{'name': '123', 'price': 1}, {'name': 'abc', 'price': 1.25}]
    return render_template('temp',
                           product_list=products,
                           user_name="hasfly"
                           )

app.addStatic('static') #设置静态资源目录,顺序无所谓，可以设置多个

@app.errorhandler(404)
def page_not_found(request):
    return Response('我是404错误')

# urlparse
if __name__ == '__main__':
    app.run('127.0.0.1', 5000, use_debugger=True, use_reloader=False)

