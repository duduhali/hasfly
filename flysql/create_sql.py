from flysql import DatetimeField
import datetime

'''获取自身的查询条件(where后面的条件), 有主键时返回所有主键，没主键时返回所有字段'''
def self_condition(self):
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
    # condition 为空时(存在主键却为空)返回'', 否则返回 ' where %s'%' and '.join(condition)
    return '' if len(condition)==0 else ' where %s'%' and '.join(condition)

'''转换要更新的数据'''
def convert_data(self,mappings):
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
def convert_condition(self,*args,**kwargs):
    __mappings = self.__mappings__
    condition = []
    operator = 'and'
    if (len(args) > 0):
        if type(args[0])==list: #判断第一个参数时不时数组
            arrs = args[0:]
        else:
            operator = args[0]
            arrs = args[1:]
        for arg in arrs:
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

'''返回通过find()开始，通过一系列设置后的SQL命令'''
def get_find_sql(cls):
    return '%s %s from %s%s%s%s;'%(cls._prefix, cls._select, cls.__table__, cls._where, cls._order, cls._limit)


'''生成sql语句的工具类，基类以MySQL为主'''
class BaseOpertion(object):
    @classmethod
    def createTable(cls, bm):
        fields = []
        for k, v in bm.__mappings__.items():
            col = '%s %s' % (v.name, v.column_type)
            if v.primary_key:
                col += ' primary key'
            if v.not_null:
                col += ' not null'
            if v.auto_increment:
                col += ' auto_increment'
            fields.append(col)
        sql_cmd = 'create table %s(%s);' % (bm.__table__, ','.join(fields))
        return sql_cmd

    @classmethod
    def save(cls,bm):
        fields = []
        args = []
        for k, v in bm.__mappings__.items():
            value = getattr(bm, k, None)
            if value == None:
                #这里认为 value 为空的字段有3种情况：1 自增类型；2 允许为空值；3 时间类型 让程序自动赋值
                if type(v) == DatetimeField :
                    value = datetime.datetime.now()
                else:
                    continue
            fields.append(v.name)
            if type(value) == int:
                args.append('%s' % value)
            else:
                args.append('"%s"' % value)
        sql_cmd = 'insert into %s (%s) values (%s);' % (bm.__table__, ','.join(fields), ','.join(args))
        return sql_cmd

    @classmethod
    def update(cls, bm):
        data = []
        for k, v in bm.__mappings__.items():
            value = getattr(bm, k, None)
            if value == None:  # 这里认为 value 空的字段是自增类型或者允许为空值
                continue
            if type(value) == int:
                data.append( '%s=%s'%(v.name,value) )
            else:
                data.append( '%s="%s"' % (v.name, value) )
        condition = self_condition(bm)
        sql_cmd = 'update %s set %s%s;' % (bm.__table__, ', '.join(data), condition)
        return sql_cmd

    @classmethod
    def delete(cls, bm):
        condition = self_condition(bm)
        sql_cmd = 'delete from %s%s;' % (bm.__table__, condition)
        return sql_cmd


    @classmethod
    def find(cls, bm): # 初始化查询参数
        bm._prefix = "select"
        bm._select = "*"
        bm._where = ""
        bm._order = ""
        bm._limit = ""

    @classmethod
    def distinct(cls, bm):
        bm._prefix += " distinct"

    @classmethod
    def select(cls, bm, cols):
        bm._select = cols

    @classmethod
    def where(cls, bm, *args, **kwargs):
        condition = convert_condition(bm, *args, **kwargs)
        if bm._where == "":  # 考虑where多次调用的情况
            bm._where = ' where %s' % condition
        else:
            bm._where += ' and %s' % condition

    @classmethod
    def order(cls, bm, *args, **kwargs):
        mappings = bm.__mappings__
        condition = []
        if (len(args) > 0):
            for arg in args:
                condition.append('%s %s' % (mappings[arg].name, 'asc'))  # 默认asc
        if (len(kwargs) > 0):
            for k, v in kwargs.items():
                condition.append('%s %s' % (mappings[k].name, v))
        bm._order = " order by %s" % (', '.join(condition))

    @classmethod
    def limit(cls, bm, offset, rows):
        if rows == None:
            bm._limit = " limit %s" % (offset)
        else:
            bm._limit = " limit %s,%s" % (offset, rows)

    @classmethod
    def all(cls, bm):
        return  get_find_sql(bm)

    @classmethod
    def one(cls, bm):
        bm.limit(1)
        return get_find_sql(bm)

    @classmethod
    def count(cls, bm, cols):
        if cols.strip() != "*":
            mappings = bm.__mappings__
            cols = mappings.get(cols.strip(), None).name
        bm._select = 'count(%s)' % cols
        return get_find_sql(bm)

    @classmethod
    def sum(cls, bm, cols, f='sum'): #max min avg 公用此操作
        mappings = bm.__mappings__
        cols = mappings.get(cols.strip(), None).name
        bm._select = '%s(%s)' %(f, cols)
        return get_find_sql(bm)

    @classmethod
    def updateAll(cls, bm, mappings, *args, **kwargs):
        data = convert_data(bm, mappings)
        condition = convert_condition(bm, *args, **kwargs)
        _where = ' where %s' % condition if condition else ''
        sql_cmd = 'update %s set %s%s;' % (bm.__table__, data, _where)
        return sql_cmd

    @classmethod
    def updateOne(cls, bm, mappings, *args, **kwargs):
        data = convert_data(bm, mappings)
        condition = convert_condition(bm, *args, **kwargs)
        _where = ' where %s' % condition if condition else ''
        sql_cmd = 'update %s set %s%s limit 1;' % (bm.__table__, data, _where)
        return sql_cmd

    @classmethod
    def deleteAll(cls, bm, *args, **kwargs):
        condition = convert_condition(bm, *args, **kwargs)
        _where = ' where %s' % condition if condition else ''
        sql_cmd = 'delete from %s%s;' % (bm.__table__, _where)
        return sql_cmd

    @classmethod
    def deleteOne(cls, bm,  *args, **kwargs):
        condition = convert_condition(bm, *args, **kwargs)
        _where = ' where %s' % condition if condition else ''
        sql_cmd = 'delete from %s%s  limit 1;' % (bm.__table__, _where)
        return sql_cmd

class MysqlOpertion(BaseOpertion):
    pass

'''默认以mysql为主，需要生成与mysql不一样的sql命令需要重载'''
class SqliteOpertion(BaseOpertion):
    @classmethod
    def createTable(cls, bm):
        fields = []
        for k, v in bm.__mappings__.items():
            col = v.name
            if v.column_type == 'int':  # sqlite中int用integer
                col += ' integer'
            if v.primary_key:
                col += ' primary key'
            if v.auto_increment:  # sqlite中自增用autoincrement且不能再加not null
                col += ' autoincrement'
            elif v.not_null:
                col += ' not null'
            fields.append(col)
        sql_cmd = 'create table %s(%s);' % (bm.__table__, ','.join(fields))
        return sql_cmd



