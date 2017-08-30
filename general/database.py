import pymysql

general_table_create = 'CREATE TABLE  IF NOT EXISTS {}(' \
                       'id INT PRIMARY KEY AUTO_INCREMENT,' \
                       'link VARCHAR(3000),' \
                       'visit INT' \
                       ');'


# 配置MySQL, 返回MySQL connection
def get_conn():
    con = pymysql.connect(host='192.168.2.111',
                          port=3306,
                          user='root',
                          password='1234',
                          db='datapro',
                          charset='utf8',
                          cursorclass=pymysql.cursors.DictCursor)
    return con


# 根据表名创建表
def create_table(table_name):
    sql = general_table_create.format(table_name)
    insert_data(sql)


# 插入数据与更新数据都是同一个函数
def insert_data(sql):
    connection = get_conn()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
            cursor.close()
    finally:
        connection.close()


def insert_list(table_name, lists):
    sql = 'INSERT INTO ' + table_name + " VALUES "
    for item in lists:
        sql += str.format('(\'{}\'),', item)
    sql = sql[0: sql.__len__() - 1] + ";"
    insert_data(sql)


# fetchone()返回的是一个字典, 键为表的列名, 值为该列的值,
# 如果select的值不存在,返回空字典
def select(sql):
    connection = get_conn()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            connection.commit()
            cursor.close()
            return result
    finally:
        connection.close()


def select_top_ten(sql):
    connection = get_conn()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
            return result
    finally:
        connection.close()
