from flysql.create import OperationDb
from flysql.config_loacl import logging
import datetime
from contextlib import contextmanager

@contextmanager
def useCursor(): #管理数据库游标的上下文管理器
    conn = OperationDb.getConnect()
    cursor = conn.cursor()
    try:
        yield cursor
        cursor.close()
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(e.__str__())
    finally:
        conn.close()

#执行sql命令，成功时返回True
def executeSQL(sql_cmd):
    result = False
    with useCursor() as cursor:
        cursor.execute(sql_cmd)
        result = True
    return result

#执行sql命令并返回封装为对象的数据
def queryData(sql_cmd,dm):
    fields = [k for k, _ in dm.__mappings__.items()]
    field_lenght = len(fields)
    data = []
    with useCursor() as cursor:
        cursor.execute(sql_cmd)
        for row in cursor.fetchall():
            kwargs = dict()
            for i in range(field_lenght):
                value = row[i]
                if type(value) == datetime.datetime:
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                kwargs[fields[i]] = value
            one = dm(**kwargs)
            one.__exist__ = True
            data.append(one)
    return data

#执行sql命令并返回一个数字
def queryNumber(sql_cmd):
    result = None
    with useCursor() as cursor:
        cursor.execute(sql_cmd)
        result = cursor.fetchone()
    return result[0] if type(result) == tuple else result
