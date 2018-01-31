# coding=utf-8
import re
import logging
from bs4 import BeautifulSoup
import datetime
import time

from customize_website.Crawler import Crawler
from customize_website.Util import Util


def main(run):
    if run:
        hqts = HuanQiuTanSuo()
        hqts.crawl()
        cxqy = ChuangXinQianYan()
        cxqy.crawl()
        jfdh = JianFengDuiHua()
        jfdh.crawl()
        sjsd = ShuJuShiDai()
        sjsd.crawl()
        mrgz = MeiRiGuanZhu()
        mrgz.crawl()


class HuanQiuTanSuo(Crawler):

    def __init__(self):
        super().__init__()
        self.url = "http://innovation.ifeng.com/discovery2014/list_0/{}.shtml"
        self.item_path = "凤凰创新->环球探索"           # 爬取网站的所在栏目
        self.relative_path = "FengHuangChuangXin/HuanQiuTanSuo/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.cookie_dict = {}

    def crawl(self):
        try:
            start = 1
            while 1:
                url_new = self.url.format(start)
                content = self.get_req(url_new)
                bs_obj = BeautifulSoup(content, "lxml")
                news_list = bs_obj.find("div", class_="newsList")
                links = news_list.findAll("a")
                for link in links:
                    url = link.get("href")
                    try:
                        if self.match_link(url):
                            self.get_link_data(url)
                    except:
                        pass
                start += 1
        except BaseException as e:
            logging.error("Get link error. URL=%s, errormsg = %s" % (url_new, str(e)))

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "lxml")
            title = bs_obj.title.get_text()
            publish_time = Util.all_strip(bs_obj.find("div", id="artical_sth").find("span").get_text())
            date_format = "%Y年%m月%d日%H:%M"
            publish_time = datetime.datetime.strptime(publish_time, date_format).strftime(self.date_format)
            page_view = 0
            content_tag = bs_obj.find("div", id="main_content")
            body_content = Util.get_content_from_tag(content_tag)
            return body_content, title, page_view, publish_time
        except BaseException as e:
            logging.error("Parse HTML error. ErrorMsg: %s" % str(e))
            raise BaseException()

    def match_link(self, link):
        pattern = re.compile(r"http://innovation.ifeng.com/discovery2014/detail.*")
        match = pattern.match(link)
        if match:
            return 1
        else:
            return 0


class ChuangXinQianYan(HuanQiuTanSuo):

    def __init__(self):
        super().__init__()
        self.url = 'http://innovation.ifeng.com/frontier/list_0/{}.shtml'
        self.item_path = "凤凰创新->创新前沿"
        self.relative_path = "FengHuangChuangXin/ChuangXinQianYan/"
        self.dirs = Crawler.all_file_dir + self.relative_path

    def match_link(self, link):
        pattern = re.compile(r"http://innovation.ifeng.com/frontier/detail.*")
        match = pattern.match(link)
        if match:
            return 1
        else:
            return


class JianFengDuiHua(HuanQiuTanSuo):

    def __init__(self):
        super().__init__()
        self.url = 'http://innovation.ifeng.com/talk/list_0/{}.shtml'
        self.item_path = "凤凰创新->尖峰对话"
        self.relative_path = "FengHuangChuangXin/JianFengDuiHua/"
        self.dirs = Crawler.all_file_dir + self.relative_path

    def match_link(self, link):
        pattern = re.compile(r"http://innovation.ifeng.com/talk/detail.*")
        match = pattern.match(link)
        if match:
            return 1
        else:
            return


class ShuJuShiDai(HuanQiuTanSuo):

    def __init__(self):
        super().__init__()
        self.url = 'http://innovation.ifeng.com/info/list_0/{}.shtml'
        self.item_path = "凤凰创新->尖峰对话"
        self.relative_path = "FengHuangChuangXin/ShuJuShiDai/"
        self.dirs = Crawler.all_file_dir + self.relative_path

    def match_link(self, link):
        pattern = re.compile(r"http://innovation.ifeng.com/info/detail.*")
        match = pattern.match(link)
        if match:
            return 1
        else:
            return


class MeiRiGuanZhu(HuanQiuTanSuo):

    def __init__(self):
        super().__init__()
        self.url = 'http://innovation.ifeng.com/focus/list_0/{}.shtml'
        self.item_path = "凤凰创新->尖峰对话"
        self.relative_path = "FengHuangChuangXin/MeiRiGuanZhu/"
        self.dirs = Crawler.all_file_dir + self.relative_path

    def match_link(self, link):
        pattern = re.compile(r"http://innovation.ifeng.com/focus/detail.*")
        match = pattern.match(link)
        if match:
            return 1
        else:
            return

