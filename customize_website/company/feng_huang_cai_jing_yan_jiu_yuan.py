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
        zl = ZhuanLan()
        # zl.crawl()
        bg = BaoGao()
        bg.crawl()


class ZhuanLan(Crawler):
    def __init__(self):
        super().__init__()
        self.url = "http://finance.ifeng.com/listpage/834/1/list.shtml"
        self.item_path = "凤凰财经研究院->专栏"           # 爬取网站的所在栏目
        self.relative_path = "FengHuangCaiJingYanJiuYuan/ZhuanLan/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.cookie_dict = {}

    def crawl(self):
        try:
            url = self.url
            while 1:
                content = self.get_req(url)
                bs_obj = BeautifulSoup(content, "html.parser")
                news_list = bs_obj.findAll("div", class_="item clearfix")
                for link in news_list:
                    try:
                        url_con = link.find("div", class_="text").find("a").get("href")
                        self.get_link_data(url_con)
                    except:
                        pass
                page_urls = bs_obj.find("div", class_="paging").findAll("a")
                url = ""
                for link in page_urls:
                    txt = link.get_text()
                    if "下一页" in txt:
                        url = link.get("href")
                        break
        except BaseException as e:
            logging.error("Get link error. URL=%s, errormsg = %s" % (url, str(e)))

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "html.parser")
            title = bs_obj.title.get_text()
            publish_time = Util.all_strip(bs_obj.find("span", itemprop="datePublished").get_text())
            date_format = "%Y-%m-%d%H:%M:%S"
            publish_time = datetime.datetime.strptime(publish_time, date_format).strftime(self.date_format)
            page_view = 0
            content_tag = bs_obj.find("div", id="main_content")
            body_content = Util.get_content_from_tag(content_tag)
            return body_content, title, page_view, publish_time
        except BaseException as e:
            logging.error("Parse HTML error. ErrorMsg: %s" % str(e))
            raise BaseException()

    def match_link(self, link):
        pass


class BaoGao(Crawler):
    """
    报告的内容只有四份,爬取总是失败,需要等待加载一个东西.
    """
    def __init__(self):
        super().__init__()
        self.url = "http://finance.ifeng.com/institute/report.shtml#p=1"
        self.item_path = "凤凰创新研究院->报告"
        self.relative_path = "FengHuangChuangXinYanJiuYuan/BaoGao/"
        self.dirs = Crawler.all_file_dir + self.relative_path

    def crawl(self):
        """
        报告的加载是一个动态加载,不在原始的HTML文件中,可以利用phantomjs加载到HTML文件中
        在分析HTML得到相应的数据.但是下一页的操作需要点击链接,由js获得数据.
        :return: 
        """
        try:
            start = 1
            date_format = "%Y年%m月%d日"
            url = self.url
            while start < 2:
                content = self.use_phantom_get_req(url, "ifeng.com")
                bs_obj = BeautifulSoup(content, "html.parser")
                items = bs_obj.findAll("div", class_="item clearfix")
                for item in items:
                    title = html.escape(item.find("h3").get_text())
                    time_str = Util.all_strip(item.find("p", class_="number").get_text())
                    publish_time = datetime.datetime.strptime(time_str, date_format).strftime(self.date_format)
                    content = item.find("div", class_="text").findAll("p")[1].get_text()
                    link = item.find("a", class_="downloadBtn").get("href")
                    self.make_dirs()
                    self.save_html_file(file_name=title, content=content)
                    self.save_content_file(file_name=title, content=content)
                    self.insert_data(link=link, item_path=self.item_path, html_path=self.relative_path + title + ".html",
                                     title=title, publish_time=publish_time, page_view=0)
                    logging.info("Get data success. URL=%s" % link)
                start += 1
        except BaseException as e:
            logging.error("Get link error. URL=%s, errormsg = %s" % (url, str(e)))



