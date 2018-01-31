# coding=utf-8

from bs4 import BeautifulSoup
import logging
from .database import DBUtil
from .CrawlerTag import Crawler


def main(run):
    if run:
        kr = Kr()
        kr.crawl()


class Kr(Crawler):

    def __init__(self):
        super().__init__()
        self.sql = "select id, link, title, html_path from article_link where item_path = '36氪' and publish_time " \
                   " like '%2017%'"

    def crawl(self):
        try:
            links = DBUtil.select_datas(self.sql)
            for link in links:
                try:
                    self.get_link_data(link)
                except:
                    pass
        except BaseException as e:
            logging.error("Download links error. ErrorMsg: %s" % str(e))

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "html.parser")
            tag_list = bs_obj.findAll("a", class_="kr-tag-gray")
            separate = "--"
            tag_content = ""
            for tag in tag_list:
                tag_content = tag_content + tag.get_text() + separate
            return tag_content[:-2]
        except BaseException as e:
            logging.error("Parser HTML file error. ErrorMsg: %s" % str(e))
            raise BaseException()
