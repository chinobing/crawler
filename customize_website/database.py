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
                           'publish_time VARCHAR(30));'

    @staticmethod
    def get_conn():
        if DBUtil.con:
            return DBUtil.con
        # 配置MySQL, 返回MySQL connection, 这是针对公司的MySQL数据库设置的。
        con = pymysql.connect(host='localhost',
                              port=3306,
                              user='root',
                              password='1234',
                              db='datapro',
                              charset='utf8',
                              cursorclass=pymysql.cursors.DictCursor)
        return con

    @staticmethod
    def create_table():
        # 根据表名创建表
        connection = DBUtil.get_conn()
        try:
            sql = DBUtil.general_table_create
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                cursor.close()
        except BaseException as e:
            logging.error("Create table error. SQL = " + sql)
            raise BaseException()

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
            logging.error("Insert data error. SQL = " + sql + " ErrorMsg: %s" % str(e))
            raise BaseException()

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
            raise BaseException()

    @staticmethod
    def close_conn():
        if DBUtil.con:
            try:
                DBUtil.con.close()
            except BaseException as e:
                logging.error("Close SQL connection error. ErrorMsg: %s" % str(e))

    @staticmethod
    def select_then_insert(select_sql, insert_sql):
        """
        很多数据库插入先要进行查询操作,如果不在数据库中,则插入数据
        :param select_sql: 
        :param insert_sql: 
        :return: 
        """
        result = DBUtil.select_data(sql=select_sql)
        if result:
            DBUtil.insert_data(insert_sql)