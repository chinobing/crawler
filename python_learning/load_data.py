from customize_website.database import DBUtil
import html


def load_csv_to_db():
    DBUtil.create_table()
    path = "F:\\ql_project\\datapro_html\\article_link.csv"
    sql_format = "INSERT INTO article_link(link, item_path, title, html_path," \
                 " page_view, publish_time) VALUES({}, {}, {}, {}," \
                 "{}, {})"
    f = open(path, "r", encoding="utf-8")
    while 1:
        line = f.readline()
        if len(line) == 0:
            break
        line = line.replace("\r", "").replace("\n", "")
        while not line.endswith(":00\""):
            line += f.readline().replace("\r", "").replace("\n", "")
        strs = line.split(", ")
        sql = sql_format.format(strs[0], strs[1], strs[2], strs[3], strs[4], strs[5])
        DBUtil.insert_data(sql)


if __name__ == "__main__":
    load_csv_to_db()