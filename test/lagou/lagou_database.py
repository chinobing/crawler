import pymysql.cursors

# Connection to the database
config = {
    'host': "127.0.0.1",
    'port': '3306',
    'user': 'root',
    'password': '1234',
    'db': 'datapro',
    'charset': 'utf-8',
    'cursorclass': pymysql.cursors.DictCursor
}

sql_add = "insert into lagou_link(link) VALUES(\"{}\")"
sql_sel = "select link from lagou_link where link=\"{}\""


def get_conn():
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='1234',
                                 db='datapro',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def insert_data(link):
    connection = get_conn()
    try:
        with connection.cursor() as cursor:
            sql_insert = str.format(sql_add, link)
            cursor.execute(sql_insert)
            connection.commit()
    finally:
        connection.close()


def select(link):
    connection = get_conn()
    try:
        with connection.cursor() as cursor:
            cursor.execute(str.format(sql_sel, link))
            result = cursor.fetchone()
            connection.commit()
            return result
    finally:
        connection.close()
