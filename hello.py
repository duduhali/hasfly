import pymysql
from contextlib import contextmanager


@contextmanager
def useConnect():
    print('初始化连接')
    conn = pymysql.connect("localhost", "root", "", "hasfly", charset='utf8')
    try:
        yield conn
    except Exception as e:
        print( e.__str__() )
    finally:
        print('关闭连接')
        conn.close()

with useConnect() as conn:
    print(conn.open)

print('ok')#这里正常运行