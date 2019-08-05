from flysql import IntegerField,StringField,DatetimeField
from flysql.model import Model

class Book(Model):
    id = IntegerField('id',not_null=True,primary_key=True,auto_increment=True)#主键
    name = StringField('name',200,not_null=True)
    author = StringField('author', 100, not_null=True)
    pub_house = StringField('pub_house',200)
    pub_date = DatetimeField('pub_date', not_null=True)


# Book.createTable()