import pymysql
import logging


class DBUtil(object):

    con = None

    # 多台电脑上跑,可能会每次创建表,比较麻烦,因此直接写在代码中,没有表会自动创建表.
    general_table_create = 'CREATE TABLE  IF NOT EXISTS article_link(' \
                           'id INT PRIMARY KEY AUTO_INCREMENT,'\
                           'link varchar(500) NOT NULL,' \
                           'item_path VARCHAR(100) NOT NULL,' \
                           'title VARCHAR(100) NOT NULL,' \
                           'html_path VARCHAR(200) NOT NULL,' \
                           'page_view INT DEFAULT 0,' \
                           'public_time VARCHAR(30));'

    @staticmethod
    def get_conn():
        if DBUtil.con:
            return DBUtil.con
        # 配置MySQL, 返回MySQL connection
        con = pymysql.connect(host='localhost',
                              port=3306,
                              user='root',
                              password='1234',
                              db='datapro',
                              charset='utf8',
                              cursorclass=pymysql.cursors.DictCursor)
        return con

    @staticmethod
    def create_table(table_name):
        # 根据表名创建表
        connection = DBUtil.get_conn()
        try:
            sql = DBUtil.general_table_create.format(table_name)
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                cursor.close()
        except BaseException as e:
            logging.error("Create table error. SQL = " + sql)

    @staticmethod
    def insert_data(sql):
        # 插入数据与更新数据都是同一个函数
        connection = DBUtil.get_conn()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                cursor.close()
        except BaseException as e:
            # 不知道对应MySQL的异常类型
            logging.error("Insert data error. SQL = " + sql)

    @staticmethod
    def select_data(sql):
        # fetchone()返回的是一个字典, 键为表的列名, 值为该列的值,
        # 如果select的值不存在,返回空字典
        connection = DBUtil.get_conn()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                connection.commit()
                cursor.close()
                return result
        except BaseException as e:
            logging.error("Query data error. SQL = " + sql)

    @staticmethod
    def close_conn():
        if DBUtil.con:
            DBUtil.con.close()
