from customize_website.database import DBUtil


def load_article_link():
    DBUtil.create_table()
    path = "/home/jfq/article.csv"
    sql_format = "INSERT INTO article_link(link, item_path, title, html_path," \
                 " page_view, publish_time) VALUES('{}', '{}', '{}', '{}'," \
                 "{}, '{}')"
    f = open(path, "r", encoding="utf-8")
    count = 0
    while 1:

        line = f.readline()
        if len(line) == 0:
            break
        line = line.replace("\r", "").replace("\n", "")
        while not line.endswith(":00"):
            line += f.readline().replace("\r", "").replace("\n", "")
        strs = line.split("\t")
        if count <= 103460:
            count += 1
            continue
        sql = sql_format.format(strs[1], strs[2], strs[3], strs[4], strs[5], strs[6])
        DBUtil.insert_data(sql)
        print(count)
        count += 1


def load_article_to_article_wechat():
    path = "/home/jfq/article.csv"
    sql_format = "insert into article_wechat(biz, link, title, page_view, thumb_number) " \
                 "VALUES('{}', '{}', '{}', {}, {}) "
    f = open(path, 'r')
    count = 0
    while 1:
        line = f.readline()
        if len(line) == 0:
            break
        strs = line.split("\t")
        sql = sql_format.format(strs[1], strs[3], strs[2], strs[4], strs[5])
        DBUtil.insert_data(sql)
        print(count)
        count += 1


def load_article_wechat():
    path = "/home/jfq/article_wechat.csv"
    select_sql_format = "select * from article_wechat  where link = '{}'"
    sql_format = "insert into article_wechat(biz, link, title, page_view, thumb_number) " \
                 "VALUES('{}', '{}', '{}', {}, {}) "
    f = open(path, 'r')
    count = 0
    while 1:
        line = f.readline()
        if len(line) == 0:
            break
        strs = line.split("\t")
        sql = sql_format.format(strs[1], strs[2], strs[3], strs[4], strs[5])
        select_sql = select_sql_format.format(strs[2])
        DBUtil.select_then_insert(select_sql, sql)
        print(count)
        count += 1


def load_xi_gua_gzh_link():
    path = "/home/jfq/xi_gua_gzh_link.csv"
    select_sql_format = "select * from article_wechat  where link = '{}'"
    sql_format = "insert into xi_gua_gzh_link(link) " \
                 "VALUES('{}') "
    f = open(path, 'r')
    count = 0
    while 1:
        line = f.readline()
        if len(line) == 0:
            break
        strs = line.split("\t")
        sql = sql_format.format(strs[1].replace("\n", ""))
        select_sql = select_sql_format.format(strs[1])
        DBUtil.select_then_insert(select_sql, sql)
        print(count)
        count += 1


if __name__ == "__main__":
    load_article_link()
