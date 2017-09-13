# coding=utf-8

import re
import logging
import html
from bs4 import BeautifulSoup
import datetime
import time

from customize_website.Crawler import Crawler
from customize_website.Util import Util


def main(run):
    if run:
        wz = ZiXun()
        wz.crawl()


class ChuangYe(Crawler):

    def __init__(self):
        super().__init__()
        self.url = 'http://www.youmi.cn/ymcy/1.shtml'
        self.item_path = "优米网->文章->创业"
        self.relative_path = "YouMiWang/WenZhang/ChuangYe/"
        self.dirs = Crawler.all_file_dir + self.relative_path

    def crawl(self):
        url = self.url
        try:
            while 1:
                content = self.get_req(url)
                bs_obj = BeautifulSoup(content, "html.parser")
                links = bs_obj.findAll("h2")
                for link in links:
                    href = link.find("a")
                    if href:
                        self.get_link_data(href.get("href"))
                next_tag = bs_obj.find(text="下一页").parent.get("href")
                if next_tag:
                    url = next_tag
                else:
                    break
        except BaseException as e:
            logging.error("Get link error. URL=%s, errormsg = %s" % (url, str(e)))

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "html.parser")
            title = bs_obj.title.get_text()
            publish_time = Util.all_strip(bs_obj.find("span", class_="ico_time").get_text())
            date_format = "%Y-%m-%d"
            publish_time = datetime.datetime.strptime(publish_time, date_format).strftime(self.date_format)
            page_view = 0
            content_tag = bs_obj.find("div", class_="content")
            body_content = Util.get_content_from_tag(content_tag)
            return body_content, title, page_view, publish_time
        except BaseException as e:
            logging.error("Parse HTML error. ErrorMsg: %s" % str(e))
            raise BaseException()


class ZiXun(ChuangYe):

    def __init__(self):
        super().__init__()
        self.url = 'http://www.youmi.cn/ymzx/1.shtml'
        self.item_path = "优米网->文章->咨询"
        self.relative_path = "YouMiWang/WenZhang/ZiXun/"
        self.dirs = Crawler.all_file_dir + self.relative_path
