# coding=utf-8
import os
import logging
import requests
from .database import DBUtil


class Crawler(object):

    all_file_dir = "D:\\document\\datapro_files\\"

    select_sql_format = "SELECT * FROM article_link WHERE link = \"{}\""
    insert_sql_format = "INSERT INTO article_link(link, item_path, title, html_path," \
                        " page_view, publish_time) VALUES(\"{}\", \"{}\", \"{}\", \"{}\"," \
                        "{}, \"{}\")"
    """
    针对每个网站的每个栏目,都需要继承这个类.
    此类抽象了整个过程,实现每个方法就可以了.
    """
    def __init__(self):
        self.url = None                 # 爬取网站的目录
        self.item_path = None           # 爬取网站的所在栏目
        self.dirs = None                # 需要保存的目录位置
        self.relative_path = None
        self.cookie_dict = {}

    def crawl(self):
        """
        爬取所有链接的方法
        :return:
        """
        pass

    def get_link_data(self, url):
        """
        获取链接的数据，保存HTML文档以及正文文本。
        :param url:
        :return:
        """
        # 从URL链接中取出为文件名，最后一个斜线后面的部分去掉.html就是。
        slash_pos = -1
        if url.endswith("/"):
            url = url[:len(url) - 1]
        while 1:
            tmp = url.find("/", slash_pos + 1)
            if tmp < -1:
                break
            slash_pos = tmp
        point_pos = url.find(".", slash_pos)
        if point_pos > 0:
            file_name = url[slash_pos + 1: point_pos]
        else:
            file_name = url[slash_pos + 1:]
        html_content = self.get_req(url)
        self.make_dirs()
        self.save_html_file(html_content.decode("utf-8"), file_name)
        body_content, title, page_view, publish_time = self.parse_html(html_content)
        self.save_content_file(body_content, file_name)
        self.insert_data(url, self.item_path, title,
                         self.relative_path + file_name + ".html",
                         page_view, publish_time)

    @staticmethod
    def insert_data(link, item_path, title, html_path,page_view, publish_time):
        select_sql = Crawler.select_sql_format.format(link)
        result = DBUtil.select_data(select_sql)
        if not result:
            insert_sql = Crawler.insert_sql_format.format(link, item_path, title,
                                                          html_path, page_view, publish_time)
            DBUtil.insert_data(insert_sql)

    def parse_html(self, content):
        """
        :return: 链接所在的正文, 转义所有的换行符为\n
        """
        return "", "", 0, "2000:01:01 00:00:00"

    def make_dirs(self):
        if not os.path.isdir(self.dirs):
            os.makedirs(path=self.dirs)

    def save_html_file(self, file_name, content):
        self.save_file(self.dirs + file_name + ".html", content)

    def save_content_file(self, file_name, content):
        self.save_file(self.dirs + file_name + ".txt", content)

    @staticmethod
    def save_file(path, content):
        f = open(path, "wt")
        f.writelines(content)
        f.close()

    def get_req(self, link):
        try:
            r = requests.get(link, cookies=self.cookie_dict, timeout=10)
            if not self.cookie_dict:
                self.cookie_dict = requests.utils.dict_from_cookiejar(r.cookies)
            logging.info("Get %s success." % link)
            return r.content
        except requests.ConnectTimeout:
            logging.error("Connection timeout. URL = " + link)
        except BaseException as e:
            logging.error("Get URL content error. URL = " + link + " ErrorMsg: " + str(e))
