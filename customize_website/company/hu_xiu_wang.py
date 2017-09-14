# coding=utf-8

import re
import logging
from bs4 import BeautifulSoup
import datetime
import time
import html.parser
import requests
from customize_website.Util import Util

from customize_website.Crawler import Crawler


def main(run):
    if run:
        pass


class ZiXun_DianShangXiaoFei(Crawler):

    def __init__(self):
        super().__init__()
        self.url = "https://www.huxiu.com/channel/103.html"
        self.item_path = "虎嗅网->咨询->电商消费"  # 爬取网站的所在栏目
        self.relative_path = "HuXiuWang/ZiXun/DianShangXiaoFei/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.cookie_dict = {}
        self.start_url = "https://www.huxiu.com"
        self.data = {"huxiu_hash_code": None, "page": None, "catId": "103"}

    def crawl(self):
        url_new = "https://www.huxiu.com/channel/ajaxGetMore"
        try:
            pattern = re.compile(r"huxiu_hash_code=(.*?);")
            content_pattern = re.compile(r"\"data\": \"(.*?)}}")
            url_new = self.url
            content = self.get_req(url_new).decode("utf-8")
            hash_code = pattern.findall(content)[0][0]
            self.data['huxiu_hash_code'] = hash_code
            page = 1
            while 1:
                self.data["page"] = page
                content = requests.post(url_new, data=self.data)
                content = content_pattern.findall(content.de)
                bs_obj = BeautifulSoup(content)
                links = bs_obj.findAll()
            for link in links:
                href = link.find("a", class_="transition").get("href")
                self.get_link_data(href)


        except BaseException as e:
            logging.error("Deal with link error. URL=%s, ErrorMsg:%s" % (url_new, str(e)))

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "lxml")
            title = Util.quote(bs_obj.title.get_text())
            pub_time = bs_obj.find("span", class_="titer")
            if not pub_time:
                pub_time = bs_obj.find("span", id='pub_date')
            if pub_time:
                pub_time = Util.all_strip(pub_time.get_text())
            try:
                date_format = "%Y-%m-%d%H:%M:%S"
                pub_time = datetime.datetime.strptime(pub_time, date_format).strftime(self.date_format)
            except:
                pub_time = "2000:01:01 00:00:00"
            page_view = 0
            content_tag = bs_obj.find("div", id="artibody")
            body_content = Util.get_content_from_tag(content_tag)
            return body_content, title, page_view, pub_time
        except BaseException as e:
            logging.error("Parser HTML file error. ErrorMsg: %s" % str(e))
