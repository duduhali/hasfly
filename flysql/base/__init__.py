from flysql.base.metaclass import ModelMetaclass
from flysql.create import sqlconfig


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

#定义类变量，设置生成sql语句的工具类
BaseModel.operation = sqlconfig.operation