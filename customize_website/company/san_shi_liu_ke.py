# coding=utf-8

from bs4 import BeautifulSoup
import logging
from customize_website.database import DBUtil
from customize_website.Crawler import Crawler
from customize_website.Util import Util
import datetime


def main(run):
    if run:
        kr = Kr()
        kr.crawl()


class Kr(Crawler):

    def __init__(self):
        super().__init__()
        self.start_id = 1
        self.relative_path = "36kr/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.sql = "select link from 36kr_link where id >= {} and id < {}"
        self.item_path = "36氪"  # 爬取网站的所在栏目
        self.cookie_dict = {}

    def get_ten_link(self):
        end_id = self.start_id + 10
        sql = self.sql.format(str(self.start_id), str(end_id))
        self.start_id = end_id
        return DBUtil.select_datas(sql)

    def crawl(self):
        try:
            while 1:
                links = self.get_ten_link()
                if len(links) == 0:
                    break
                for link in links:
                    try:
                        self.get_link_data(link["link"])
                    except:
                        pass
        except BaseException as e:
            logging.error("Download links error. ErrorMsg: %s" % str(e))

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "html.parser")
            title = bs_obj.title.get_text()
            pub_time = bs_obj.find("abbr", class_="time")
            if not pub_time:
                pub_time = "2000-01-01: 00:00:00"
            else:
                pub_time = Util.all_strip(pub_time.get_text())
                date_format = "%Y-%m-%d"
                pub_time = datetime.datetime.strptime(pub_time, date_format).strftime(self.date_format)
            page_view = 0
            content_tag = bs_obj.find("section", class_="textblock")
            body_content = Util.get_content_from_tag(content_tag)
            return body_content, title, page_view, pub_time
        except BaseException as e:
            logging.error("Parser HTML file error. ErrorMsg: %s" % str(e))
            raise BaseException()
