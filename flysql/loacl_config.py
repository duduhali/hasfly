import logging

'''
用户配置
'''
# db={
#     'sql':'mysql',     #指定数据库，目前支持 sqlite， mysql
#     'host':     'localhost',    #MySQL服务器地址
#     # 'port':     3306,            #MySQL服务器端口号
#     'user':     'root',         #用户名
#     'passwd':   '',             #密码
#     'db':       'hasfly',             #数据库名称
# }

db={
    'sql':'sqlite',     #指定数据库，目前支持 sqlite， mysql
    # 'database': 'sqlite.db',      #数据库为sqlite时才需要指定
}

logging.basicConfig( level=logging.INFO )
# logging.basicConfig( level=logging.WARNING )
