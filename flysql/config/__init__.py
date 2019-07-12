'''
base_mysql和base_sqlite为默认配置
'''
base_mysql={
    'host':     'localhost',    #MySQL服务器地址
    'port':     3306,            #MySQL服务器端口号
    'user':     'root',         #用户名
    'passwd':   '',             #密码
    'db':       '',             #数据库名称
    'charset': 'utf8',         #连接编码
}
base_sqlite={
    'database': 'sqlite.db'
}