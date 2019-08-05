from flysql.loacl_config import logging

class Field(object):
    #默认，False:可为空,False:不是主键，False:不自动增长(自动增长仅int型可以)
    def __init__(self,name,column_type,not_null,primary_key,auto_increment):
        self.name = name
        self.column_type = column_type
        self.not_null = not_null
        self.primary_key = primary_key
        self.auto_increment = auto_increment
    def __str__(self):
        return '<%s:%s>'%(self.__class__.__name__,self.name)

class IntegerField(Field):
    def __init__(self,name,not_null=False,primary_key=False,auto_increment=False):
        super(IntegerField,self).__init__(name,'int',not_null,primary_key,auto_increment)

class StringField(Field):
    def __init__(self,name,lenght=100,not_null=False,primary_key=False,auto_increment=False):
        super(StringField,self).__init__(name,'varchar(%d)'%lenght,not_null,primary_key,auto_increment)

class DatetimeField(Field):
    def __init__(self,name,not_null=False,primary_key=False,auto_increment=False):
        super(DatetimeField,self).__init__(name,'datetime',not_null,primary_key,auto_increment)

#元类创建的类的子类会再次调用
class ModelMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name == 'Model' or name == 'BaseModel':
            return type.__new__(cls,name,bases,attrs)
        table = name
        mappings = dict()
        for k,v in attrs.items():
            if isinstance(v,Field):
                mappings[k] = v
            elif k == '__table__':
                table = v;
        for k in mappings.keys():
            attrs.pop(k)
        #把属性从类中删除，放到mppings中
        attrs['__mappings__'] = mappings
        attrs['__table__'] = table
        return type.__new__(cls,name,bases,attrs)

class BaseModel(dict,metaclass=ModelMetaclass):
    def __init__(self,**kwargs):
        self.__exist__ = False
        super(BaseModel,self).__init__(**kwargs)
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'"%item)
    def __setattr__(self, key, value):
        self[key] = value