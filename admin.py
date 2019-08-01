from flyweb import Blueprint

admin = Blueprint('admin',__name__)
#只能使用/做分割
@admin.route('/',method=['GET'])
def index(request):
    return  'admin page'

@admin.route('/one',method=['GET'])
def index(request):
    return  'one admin'