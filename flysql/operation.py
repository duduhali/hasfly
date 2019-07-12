from flysql.baseconfig import *
from flysql.config import db

#用模块实现单例模式
class __SQLconfig(object):
    def __init__(self):
        sql = db.get('sql', 'mysql') #位置的sql类型时使用mysql
        sql_config = dict()
        if sql == 'mysql':
            import pymysql
            self.drive = pymysql #数据库驱动模块
            base_config = base_mysql
        elif sql == 'sqlite':
            import sqlite3
            self.drive = sqlite3
            base_config = base_sqlite
        else:
            raise Exception('数据库类型指定错误')

        for k, v in base_config.items():
            sql_config[k] = db.get(k, v)
        self.__sql_config = sql_config
        self.sql = sql
    def getParam(self):
        return self.__sql_config

sqlconfig = __SQLconfig()

class OperationDb(object):
    @classmethod
    def getConnect(cls):  #返回数据库链接
        # print(sqlconfig.getParam())
        conn = sqlconfig.drive.connect(** sqlconfig.getParam())
        return conn

# OperationDb.getConnect()

