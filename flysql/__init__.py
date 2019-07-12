from flysql.field import Field,IntegerField,StringField,DatetimeField
from flysql.base import BaseModel
from flysql.config import *
from flysql.operation import sqlconfig,OperationDb

import logging

logging.basicConfig( level=logging.INFO )
# logging.basicConfig( level=logging.WARNING )

#执行sql命令，成功返回True
def executeSQL(sql_cmd):
    conn = OperationDb.getConnect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_cmd)
        logging.info('cursor.rowcount   %s' % cursor.rowcount)
        cursor.close()
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        logging.error(e.__str__())
        return False

    conn.close()
    return True

class Model(BaseModel):
    def save(self):
        fields = []
        args = []
        for k,v in self.__mappings__.items():
            value = getattr(self,k,None)
            if value == None or v.primary_key:
                continue
            fields.append(v.name)
            if type(value) == int:
                args.append('%s'% value)
            else:
                args.append('"%s"'%value)
        sql_cmd = 'insert into %s (%s) values (%s);'%(self.__table__,','.join(fields),','.join(args))
        logging.info('插入数据   %s' % sql_cmd)
        return executeSQL(sql_cmd)

    def delete(self):
        condition = self._self_condition()
        sql_cmd = 'delete from %s%s;' % (self.__table__, condition)
        logging.info('删除数据   %s' % sql_cmd)
        return executeSQL(sql_cmd)

    def update(self,mappings):
        data = self._convert_data(mappings)
        condition = self._self_condition()
        sql_cmd = 'update %s set %s%s;' % (self.__table__, data,condition)
        logging.info('更新数据   %s' % sql_cmd)
        return executeSQL(sql_cmd)



    @classmethod
    def createTable(cls):  # 创建表
        # 这里这样实现比较别扭，以后再优化
        sql = sqlconfig.sql
        if sql == 'mysql':
            sql_cmd = cls.mysqlCreateTable()
        elif sql == 'sqlite':
            sql_cmd = cls.sqliteCreateTable()
        logging.info('创建表=>%s'%sql_cmd)
        return executeSQL(sql_cmd)


    @classmethod
    def sqliteCreateTable(cls):
        fields = []
        for k, v in cls.__mappings__.items():
            col = v.name
            if v.column_type =='int': #sqlite中int用integer
                col += ' integer'
            if v.primary_key:
                col +=' primary key'
            if v.auto_increment:        #sqlite中自增用autoincrement且不能再加not null
                col +=' autoincrement'
            elif v.not_null:
                col +=' not null'
            fields.append(col)
        sql_cmd = 'create table %s(%s);'%(cls.__table__, ','.join(fields))
        return sql_cmd

    @classmethod
    def mysqlCreateTable(cls):
        fields = []
        for k, v in cls.__mappings__.items():
            col = '%s %s'%(v.name,v.column_type)
            if v.primary_key:
                col += ' primary key'
            if v.not_null:
                col += ' not null'
            if v.auto_increment:  # sqlite中自增用autoincrement且不能再加not null
                col += ' auto_increment'
            fields.append(col)
        sql_cmd = 'create table %s(%s);' % (cls.__table__, ','.join(fields))
        return sql_cmd
