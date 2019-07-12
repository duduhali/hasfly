from test import User

# u = User(name='dudu',data='2019-07-01 22:10',age=22)#参数的顺序可以任意
# print(u)

k = {'id': 4, 'age': 22, 'name': 'dudu', 'data': '2019-07-01 22:10', 'updatetime': '2019-07-01 22:10'}
# u2 = u.__class__(**k)
# print(u2)

u3 = User(**k)
print(u3)
print(type(User),type(u3))