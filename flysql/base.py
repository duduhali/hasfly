from flysql.metaclass import ModelMetaclass

class BaseModel(dict,metaclass=ModelMetaclass):
    def __init__(self,**kwargs):
        super(BaseModel,self).__init__(**kwargs)
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'"%item)
    def __setattr__(self, key, value):
        self[key] = value

    '''获取自身的查询条件(where后面的条件), 有主键时只返回主键，没主键时返回所有字段'''
    def _self_condition(self):
        condition = []
        primary_key_tag = False
        for k, v in self.__mappings__.items():
            if v.primary_key:
                primary_key_tag = True
            value = getattr(self, k, None)
            if value == None or (primary_key_tag and v.primary_key==False):
                continue
            if type(value) == int:
                condition.append('%s=%s' % (v.name, value))
            else:
                condition.append('%s="%s"' % (v.name, value))
        return '' if len(condition)==0 else ' where %s'%' and '.join(condition)

    '''转换要更新的数据'''
    def _convert_data(self,mappings):
        data = []
        for k, v in self.__mappings__.items():
            arg = mappings.get(k, None)
            if arg != None:  # 只处理数据表中存在的字段
                if type(arg) == int:
                    data.append('%s=%s' % (v.name, arg))
                else:
                    data.append('%s="%s"' % (v.name, arg))
        return ','.join(data)

    '''转换传入的查询条件(where后面的条件)'''
    def _convert_condition(self,*args,**kwargs):
        __mappings = self.__mappings__
        condition = []
        operator = 'and'
        if (len(args) > 0):
            operator = args[0]
            for arg in args[1:]:
                # arg = ['>', 'age', 22]
                field = __mappings.get(arg[1])
                if type(arg[2]) == int:
                    condition.append('%s %s %s' % (field.name, arg[0], arg[2]))
                else:
                    condition.append('%s %s "%s"' % (field.name, arg[0], arg[2]))
        if (len(kwargs) > 0):
            for k, v in kwargs.items():
                field = __mappings.get(k)
                if type(v) == int:
                    condition.append('%s = %s' % (field.name, v))
                elif type(v) == list:
                    # 转换数据，[22, 'name'] => ['22', '"name"']
                    v = list(map(lambda i: str(i) if type(i) == int else '"%s"' % i, v))
                    condition.append('%s in (%s)' % (field.name, ','.join(v)))
                else:
                    condition.append('%s = "%s"' % (field.name, v))
        return (' %s ' % operator).join(condition)



    # 类方法
    @classmethod
    def find(cls):  # 初始化查询参数
        cls._prefix = "select"
        cls._select = "*"
        cls._where = ""
        cls._order = ""
        cls._limit = ""
        # DISTINCT
        return cls

    @classmethod
    def distinct(cls):
        cls._prefix += " distinct"
        return cls

    @classmethod
    def select(cls, select):
        cls._select = select
        return cls

    @classmethod
    def where(cls, *args, **kwargs):
        condition = cls._convert_condition(cls, *args, **kwargs)
        if cls._where == "":  # 考虑where多次调用的情况
            cls._where = 'where %s' % condition
        else:
            cls._where += ' and %s' % condition
        return cls

    @classmethod
    def order(cls, *args, **kwargs):
        condition = []
        if (len(args) > 0):
            for arg in args:
                condition.append('%s %s' % (arg, 'asc'))  # 默认asc
        if (len(kwargs) > 0):
            for k, v in kwargs.items():
                condition.append('%s %s' % (k, v))
        cls._order = "order by %s" % (', '.join(condition))
        return cls

    @classmethod
    def limit(cls, offset=0, rows=None):
        if rows == None:
            cls._limit = "limit %s" % (offset)
        else:
            cls._limit = "limit %s,%s" % (offset, rows)
        return cls

    @classmethod
    def _get_sql(cls):
        return '%s %s from %s %s %s %s;' % (
        cls._prefix, cls._select, cls.__table__, cls._where, cls._order, cls._limit)

    @classmethod
    def all(cls):
        sql = cls._get_sql()
        print('SQL: %s' % sql)  #
        return []

    @classmethod
    def one(cls):
        cls.limit(1)
        sql = cls._get_sql()
        print('SQL: %s' % sql)  #

    @classmethod
    def count(cls, select='*'):  # 返回行数
        cls._select = 'count(%s)' % select
        sql = cls._get_sql()
        print('SQL: %s' % sql)  #

    @classmethod
    def sum(cls, select='*'):  # 返回行数 类似的还有 max min avg
        cls._select = 'sum(%s)' % select
        sql = cls._get_sql()
        print('SQL: %s' % sql)  #

    @classmethod
    def updateAll(cls, mappings, *args, **kwargs):
        data = cls._convert_data(cls, mappings)
        condition = cls._convert_condition(cls, *args, **kwargs)
        _where = ' where %s' % condition if condition else ''
        sql = 'update %s set %s%s;' % (cls.__table__, data, _where)
        print('SQL: %s' % sql)  #

    @classmethod
    def updateOne(cls, mappings, *args, **kwargs):
        data = cls._convert_data(cls, mappings)
        condition = cls._convert_condition(cls, *args, **kwargs)
        _where = ' where %s' % condition if condition else ''
        sql = 'update %s set %s%s limit 1;' % (cls.__table__, data, _where)
        print('SQL: %s' % sql)  #

    @classmethod
    def deleteAll(cls, *args, **kwargs):  # condition为None时删除所有
        condition = cls._convert_condition(cls, *args, **kwargs)
        _where = ' where %s' % condition if condition else ''
        sql = 'delete from %s%s;' % (cls.__table__, _where)
        print('SQL: %s' % sql)  #

    @classmethod
    def deleteOne(cls, *args, **kwargs):
        condition = cls._convert_condition(cls, *args, **kwargs)
        _where = ' where %s' % condition if condition else ''
        sql = 'delete from %s%s  limit 1;' % (cls.__table__, _where)
        print('SQL: %s' % sql)  #

