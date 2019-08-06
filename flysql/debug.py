from flysql import IntegerField,StringField,DatetimeField

from flysql.model import Model



class User(Model):
    '''
        可以一个或多个主键或者没有主键
        下面的Field字段的顺序不能变，若变了需要重新生成表或者手动修改表
    '''
    __table__ = 'user' #指定表明，默认类名为表名
    id = IntegerField('id',not_null=True,primary_key=True,auto_increment=True)#主键
    age= IntegerField('age_id') # age_id为数据库中的字段名
    name = StringField('username',100,not_null=True)
    data = DatetimeField('time',not_null=True) #日期类型数据若不能为空且在插入时未赋值，则用当前时间自动赋值
    updatetime = DatetimeField('updatetime', not_null=True)


# User.createTable()

# u = User( name='dudu',data='2019-07-01 22:10',age=22)#参数的顺序可以任意
# print( u.save() )
# u.name = 'yang'
# u.id=1
# u.__exist__ = True
# u.update()
# u.delete()


result = User.find().all()
for one in result:
    print(one)

# result = User.find().where('or',name='yang',age=[22]).order('age').one()
# print(result)

# result = User.find().where(name='dudu',age=22).order(age='asc',name='desc').limit(0,1).all()
# print(result)
# result = User.find().where('or',['>=','age',22],name='yang').distinct().all()
# print(result)

# print(User.find().where(name='dudu').count('age'))
# print(User.find().where(name='dudu').sum('age'))
# print(User.find().where(name='dudu').max('id'))
# print(User.find().where(name='dudu').min('id'))
# print(User.find().where(name='dudu').avg('id'))

# User.updateAll({'age':22})
# User.updateAll({'age':22},name='yang',age=50)

# import sqlite3
# print(sqlite3.sqlite_version)  查看SQLite版本  py3.6 SQLite是3.14.2

# User.updateOne({'age':50},'or',name='dudu',age=[22,23])
# User.updateOne({'age':22},'or',['>','age',22],name='yang')
# User.deleteAll(name='yang',age=50)
# User.deleteOne('or',['>','age',22],name='yang')

# print( queryOther('select * from user') )