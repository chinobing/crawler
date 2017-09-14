# coding=utf-8

import re
import logging
from bs4 import BeautifulSoup
import datetime
import time
import html.parser
from customize_website.Util import Util

from customize_website.Crawler import Crawler


def main(run):
    if run:
        # gdxn = HuLianWang_GunDongXinWen()
        # gdxn.crawl()
        csj = ChuangShiJi()
        csj.crawl()

class ChuangYe_GunDongXinWen(Crawler):
    def __init__(self):
        super().__init__()
        self.item_path = "新浪科技->创业->滚动新闻"
        self.relative_path = "XinLangKeJi/ChuangYe/GunDongXinWen/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.url = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php' \
                   '?col=365&spec=&type=&date={}&ch=05&k=&offset_page=0' \
                   '&offset_num=0&num=60&asc=&page=1'

    def crawl(self):
        date_format = "%Y-%m-%d"
        date_start = datetime.datetime.strptime("2015-07-29", date_format)
        date_end = datetime.datetime.now()
        date_dlt = datetime.timedelta(days=1)
        pattern = re.compile("(http://.*?)\"")
        while 1:
            date_dif = date_end - date_start
            if date_dif.days < 0:
                break
            url = self.url.format(date_start.strftime(date_format))
            content_byte = self.get_req(url)
            try:
                content = content_byte.decode("gbk")
            except:
                try:
                    content = content_byte.decode("utf-8")
                except:
                    logging.error("Can't decode with gbk and utf-8")
                    raise BaseException()
            # code_dict = chardet.detect(content_byte)
            # try:
            #     content = content_byte.decode(code_dict["encoding"])
            # except BaseException as e:
            #     logging.error("Decode content error. ErrorMsg: %s" % str(e))
            #     raise BaseException()
            link_list = pattern.findall(content)
            for link in link_list:
                self.get_link_data(link)
            time.sleep(3)
            date_start += date_dlt

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "lxml")
            title = bs_obj.title.get_text()
            publish_time = bs_obj.find("span", class_="titer")
            if not publish_time:
                publish_time = bs_obj.find("span", id="pub_date")
            publish_time = publish_time.get_text().replace(u"\xa0", "").replace(" ", "")
            date_format = "%Y年%m月%d日%H:%M"
            publish_time = datetime.datetime.strptime(publish_time, date_format).strftime(self.date_format)
            page_view = 0
            content_tag = bs_obj.find("div", id="artibody")
            [script.extract() for script in content_tag.findAll("script")]
            [style.extract() for style in content_tag.findAll("style")]
            return content_tag.get_text(), title, page_view, publish_time
        except BaseException as e:
            logging.error("Parse content error. ErrorMsg: " + str(e))
            raise BaseException()

    def match_link(self, link):
        if "sina.com" in link:
            return 1
        else:
            return 0


class HuLianWang_GunDongXinWen(Crawler):

    def __init__(self):
        super().__init__()
        self.item_path = "新浪科技->互联网->滚动新闻"
        self.relative_path = "XinLangKeJi/HuLianWang/GunDongXinWen/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.url = 'http://roll.tech.sina.com.cn/internet_all/index_1.shtml'
        self.page_url_prefix = 'http://roll.tech.sina.com.cn/internet_all/'

    def crawl(self):
        url = self.url
        try:
            while 1:
                content = self.get_req(url)
                bs_obj = BeautifulSoup(content, "lxml")
                cont_list = bs_obj.find("div", class_="contList").findAll("a")
                for link in cont_list:
                    href = link.get("href")
                    try:
                        self.get_link_data(href)
                    except:
                        pass
                next_url = bs_obj.find("span",  class_="pagebox_next").find('a')
                if not next_url:
                    break
                url = self.page_url_prefix + next_url.get("href")[2:]
        except BaseException as e:
            logging.error("Deal with link error. URL=%s, ErrorMsg:%s" % (url, str(e)))

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
                date_format = "%Y年%m月%d日%H:%M"
                pub_time = datetime.datetime.strptime(pub_time, date_format).strftime(self.date_format)
            except:
                pub_time = "2000:01:01 00:00:00"
            page_view = 0
            content_tag = bs_obj.find("div", id="artibody")
            body_content = Util.get_content_from_tag(content_tag)
            return body_content, title, page_view, pub_time
        except BaseException as e:
            logging.error("Parser HTML file error. ErrorMsg: %s" % str(e))


class ChuangShiJi(Crawler):

    def __init__(self):
        super().__init__()
        super().__init__()
        self.item_path = "新浪科技->互联网->创事记"
        self.relative_path = "XinLangKeJi/HuLianWang/ChuangShiJi/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=402&lid=2559&num=20&versionNumber=1.2.8&page={}&encode=utf-8&callback=feedCardJsonpCallback&_={}'

    def crawl(self):
        try:
            pattern = re.compile(r'(http:[^,]*?\.s?html?)')
            start = 1
            while 1:
                url_new = self.url.format(start, int(float(time.time())*1000))
                content = self.get_req(url_new).decode("utf-8")
                links = pattern.findall(html.parser.HTMLParser().unescape(content))
                if len(links) == 0:
                    break
                links_set = set()
                for link in links:
                    if ".d" in link or link in links_set:
                        continue
                    links_set.add(link.replace("\\", ""))
                for link in links_set:
                    self.get_link_data(link)
                start += 1
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