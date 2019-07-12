from flysql import Model,IntegerField,StringField,DatetimeField

class User(Model): #可以一个或多个主键或者没有主键
    __table__ = 'user' #指定表明，默认类名为表名
    id = IntegerField('id',not_null=True,primary_key=True,auto_increment=True)#主键
    age= IntegerField('age_id') # age_id为数据库中的字段名
    name = StringField('username',100,not_null=True)
    data = DatetimeField('time',not_null=True)

# User.createTable()

u = User(name='dudu',data='2019-07-01 22:10',age=22)#参数的顺序可以任意
# u.save()
# u.name = 'yang'
u.delete()
# u.update({'name':'yang','age':22})


# User.find().select("name,age").where(name='yang',age=22).order(age='asc',name='desc').limit(1,5).all()
# User.find().select("name").where('or',name='yang',age=[22,23]).order('age').one()
# User.find().where('or',['>','age',22],name='yang').distinct().all()
# User.find().where(name='yang').where(age=10).all()
# User.find().where(name='yang').where(age=10).count()

# User.updateAll({'age':22})
# User.updateAll({'age':22},name='yang',age=50)
# User.updateOne({'age':22},'or',name='yang',age=[22,23])
# User.updateOne({'age':22},'or',['>','age',22],name='yang')
# User.deleteAll(name='yang',age=50)
# User.deleteOne('or',['>','age',22],name='yang')
# User.sqliteCreateTable()
User.mysqlCreateTable()