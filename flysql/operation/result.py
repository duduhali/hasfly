from flysql.create import OperationDb
from flysql.config_loacl import logging
import datetime


#执行sql命令，成功时返回True
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

#执行sql命令并返回封装为对象的数据
def queryData(sql_cmd,dm):
    data = []
    mappings = dm.__mappings__
    fields = []
    for k, _ in mappings.items():
        fields.append(k)
    field_lenght = len(fields)

    conn = OperationDb.getConnect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_cmd)
        results = cursor.fetchall()
        for row in results:
            kwargs = dict()
            for i in range(field_lenght):
                value = row[i]
                if type(value)==datetime.datetime:
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                kwargs[fields[i]] = value
            one = dm(**kwargs)
            one.__exist__ = True
            data.append(one)
        cursor.close()
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        logging.error(e.__str__())
        return None
    conn.close()
    return data

#执行sql命令并返回原始数据
def queryOther(sql_cmd):
    results = None
    conn = OperationDb.getConnect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_cmd)
        results = cursor.fetchall()
        cursor.close()
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        logging.error(e.__str__())
        return None
    conn.close()
    return results
