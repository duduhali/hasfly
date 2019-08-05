from flysql import logging,BaseModel
from flysql.create_db import sqlconfig
from flysql.do_query import executeSQL,queryData,queryNumber

class Model(BaseModel):
    @classmethod
    def createTable(cls):  # 创建表
        sql_cmd = cls.operation.createTable(cls)  #生成sql语句
        logging.info('创建表=>%s' % sql_cmd)
        return executeSQL(sql_cmd)

    def save(self):
        sql_cmd = self.operation.save(self)  # 生成sql语句
        logging.info('插入   %s' % sql_cmd)
        return executeSQL(sql_cmd)

    def update(self):
        if self.__exist__ == False:
            return self.save()   #不是从表中取出的数据, 更新时返回保存的sql名
        sql_cmd = self.operation.update(self)  # 生成sql语句
        logging.info('更新   %s' % sql_cmd)
        return executeSQL(sql_cmd)

    def delete(self):
        if self.__exist__ == False:
            logging.warning('删除失败,__exist__ = False')
            return False   #不是从表中取出的数据, 直接返回False
        sql_cmd = self.operation.delete(self)  # 生成sql语句
        logging.info('删除   %s' % sql_cmd)
        return executeSQL(sql_cmd)

    @classmethod
    def find(cls):
        cls.operation.find(cls)
        return cls

    @classmethod
    def distinct(cls):
        cls.operation.distinct(cls)
        return cls

    # @classmethod       此方法有问题
    # def select(cls, cols):
    #     cls.operation.select(cls,cols)
    #     return cls

    @classmethod
    def where(cls, *args, **kwargs):
        cls.operation.where(cls, *args, **kwargs)
        return cls

    @classmethod
    def order(cls, *args, **kwargs):
        cls.operation.order(cls, *args, **kwargs)
        return cls

    @classmethod
    def limit(cls, offset=0, rows=None):
        cls.operation.limit(cls, offset, rows)
        return cls

    @classmethod
    def all(cls):
        sql_cmd = cls.operation.all(cls)  # 生成sql语句
        logging.info('数据(all)   %s' % sql_cmd)
        return queryData(sql_cmd,cls)

    @classmethod
    def one(cls):
        sql_cmd = cls.operation.one(cls)  # 生成sql语句
        logging.info('数据(one)   %s' % sql_cmd)
        data = queryData(sql_cmd, cls)
        return data[0]  if data!=None and len(data)>0 else None   #查询结果为零时返回None

    @classmethod
    def count(cls, cols='*'):  # 参数可以是"*"或者是一个字段
        sql_cmd = cls.operation.count(cls,cols)  # 生成sql语句
        logging.info('数量   %s' % sql_cmd)
        return queryNumber(sql_cmd)

    @classmethod
    def sum(cls, cols):  # 参数不能是'*'且只能传入一个字段返回行数 类似的还有 max min avg
        sql_cmd = cls.operation.sum(cls, cols)  # 生成sql语句
        logging.info('总和   %s' % sql_cmd)
        return queryNumber(sql_cmd)
    @classmethod
    def max(cls, cols):  # 参数不能是'*'且只能传入一个字段返回行数
        sql_cmd = cls.operation.sum(cls, cols, 'max')  # 生成sql语句
        logging.info('总和   %s' % sql_cmd)
        return queryNumber(sql_cmd)

    @classmethod
    def min(cls, cols):  # 参数不能是'*'且只能传入一个字段返回行数
        sql_cmd = cls.operation.sum(cls, cols, 'min')  # 生成sql语句
        logging.info('总和   %s' % sql_cmd)
        return queryNumber(sql_cmd)

    @classmethod
    def avg(cls, cols):  # 参数不能是'*'且只能传入一个字段返回行数
        sql_cmd = cls.operation.sum(cls, cols, 'avg')  # 生成sql语句
        logging.info('总和   %s' % sql_cmd)
        return queryNumber(sql_cmd)

    @classmethod
    def updateAll(cls, mappings, *args, **kwargs):
        sql_cmd = cls.operation.updateAll(cls, mappings, *args, **kwargs)  # 生成sql语句
        logging.info('updateAll   %s' % sql_cmd)
        return executeSQL(sql_cmd)

    @classmethod
    def updateOne(cls, mappings, *args, **kwargs):
        sql_cmd = cls.operation.updateOne(cls, mappings, *args, **kwargs)  # 生成sql语句
        logging.info('updateOne   %s' % sql_cmd)
        return executeSQL(sql_cmd)

    @classmethod
    def deleteAll(cls, *args, **kwargs):  # condition为None时删除所有
        sql_cmd = cls.operation.deleteAll(cls, *args, **kwargs)  # 生成sql语句
        logging.info('deleteAll   %s' % sql_cmd)
        return executeSQL(sql_cmd)

    @classmethod
    def deleteOne(cls, *args, **kwargs):
        sql_cmd = cls.operation.deleteOne(cls, *args, **kwargs)  # 生成sql语句
        logging.info('deleteOne   %s' % sql_cmd)
        return executeSQL(sql_cmd)

#定义类变量，设置生成sql语句的工具类
Model.operation = sqlconfig.operation