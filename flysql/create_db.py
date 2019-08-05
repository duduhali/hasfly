from flysql.default import base_mysql,base_sqlite
from flysql.loacl_config import db
from flysql.create_sql import MysqlOpertion,SqliteOpertion

#用模块实现单例模式
class __SQLconfig(object):
    def __init__(self):
        sql = db.get('sql', 'mysql') #位置的sql类型时使用mysql
        config_param = dict()
        if sql == 'mysql':
            import pymysql
            self.drive = pymysql #数据库驱动模块
            base_config = base_mysql #数据库默认连接参数
            self.operation = MysqlOpertion #负责生产sql命令的工具类
        elif sql == 'sqlite':
            import sqlite3
            self.drive = sqlite3
            base_config = base_sqlite
            self.operation = SqliteOpertion
        else:
            raise Exception('数据库类型指定错误')

        for k, v in base_config.items():    #生成当前数据库连接参数
            config_param[k] = db.get(k, v)
        self.__config_param = config_param
    def getParam(self):
        return self.__config_param

sqlconfig = __SQLconfig()

class OperationDb(object):
    @classmethod
    def getConnect(cls):  #返回数据库链接
        # print(sqlconfig.getParam())
        conn = sqlconfig.drive.connect(** sqlconfig.getParam())
        return conn
