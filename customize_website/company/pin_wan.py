import logging
from bs4 import BeautifulSoup
import datetime

from customize_website.Crawler import Crawler
from customize_website.Util import Util


def main(run):
    if run:
        # rw = ZiXun_RenWu()
        # rw.crawl()
        td = ZiXun_TaiDu()
        td.crawl()
        xw = ZiXun_XinWen()
        xw.crawl()
        zh = ZiXun_ZhiShi()
        zh.crawl()
        cp = ZiXun_ChanPin()
        cp.crawl()
        gs = ZiXun_GongSi()
        gs.crawl()


class ZiXun_RenWu(Crawler):
    def __init__(self):
        super().__init__()
        self.url = "http://www.pingwest.com/category/figure/"
        self.item_path = "品玩->咨询->人物"           # 爬取网站的所在栏目
        self.relative_path = "PinWan/ZiXun/RenWu/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.cookie_dict = {}

    def crawl(self):
        try:
            url = self.url
            while 1:
                content = self.get_req(url)
                bs_obj = BeautifulSoup(content, "html.parser")
                news_list = bs_obj.find("div", class_="news-list").findAll("h2", class_="title")
                for link in news_list:
                    try:
                        url_con = link.find("a").get("href")
                        self.get_link_data(url_con)
                    except:
                        pass
                url = bs_obj.find("a", class_="next page-numbers")
                if not url:
                    break
                else:
                    url = url.get("href")
        except BaseException as e:
            logging.error("Get link error. URL=%s, errormsg = %s" % (url, str(e)))

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "html.parser")
            title = bs_obj.title.get_text()
            publish_time = Util.all_strip(bs_obj.find("span", class_="post-time").get_text())
            if "天" in publish_time:
                pos = publish_time.index("天")
                days = datetime.timedelta(int(publish_time[:pos]))
                publish_time = (datetime.datetime.now() - days).strftime(self.date_format)
            elif "小时" in publish_time:
                pos = publish_time.index("小")
                days = datetime.timedelta(int(publish_time[:pos]) // 24 + 1)
                publish_time = (datetime.datetime.now() - days).strftime(self.date_format)
            else:
                date_format = "%Y-%m-%d"
                publish_time = datetime.datetime.strptime(publish_time, date_format).strftime(self.date_format)
            page_view = 0
            content_tag = bs_obj.find("div", id="sc-container")
            post_footer = content_tag.find("p", class_="post-footer-wx")    # 删除不需要的内容
            if post_footer:
                post_footer.extract()
            block_quote = content_tag.find("blockquote")                     # 删除不需要的内容
            if block_quote:
                block_quote.extract()
            body_content = Util.get_content_from_tag(content_tag)
            return body_content, title, page_view, publish_time
        except BaseException as e:
            logging.error("Parse HTML error. ErrorMsg: %s" % str(e))
            raise BaseException()

    def match_link(self, link):
        pass


class ZiXun_TaiDu(ZiXun_RenWu):
    def __init__(self):
        super().__init__()
        self.url = "http://www.pingwest.com/category/attitude/"
        self.item_path = "品玩->咨询->态度"           # 爬取网站的所在栏目
        self.relative_path = "PinWan/ZiXun/TaiDu/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.cookie_dict = {}


class ZiXun_XinWen(ZiXun_RenWu):
    def __init__(self):
        super().__init__()
        self.url = "http://www.pingwest.com/category/news/"
        self.item_path = "品玩->咨询->新闻"           # 爬取网站的所在栏目
        self.relative_path = "PinWan/ZiXun/XinWen/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.cookie_dict = {}


class ZiXun_ZhiShi(ZiXun_RenWu):
    def __init__(self):
        super().__init__()
        self.url = "http://www.pingwest.com/category/knowledge/"
        self.item_path = "品玩->咨询->知识"           # 爬取网站的所在栏目
        self.relative_path = "PinWan/ZiXun/ZhiShi/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.cookie_dict = {}


class ZiXun_ChanPin(ZiXun_RenWu):
    def __init__(self):
        super().__init__()
        self.url = "http://www.pingwest.com/category/product/"
        self.item_path = "品玩->咨询->产品"           # 爬取网站的所在栏目
        self.relative_path = "PinWan/ZiXun/ChanPin/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.cookie_dict = {}


class ZiXun_GongSi(ZiXun_RenWu):
    def __init__(self):
        super().__init__()
        self.url = "http://www.pingwest.com/category/company/"
        self.item_path = "品玩->咨询->公司"           # 爬取网站的所在栏目
        self.relative_path = "PinWan/ZiXun/GongSi/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.cookie_dict = {}


class ZhuanTi(Crawler):

    def __init__(self):
        super().__init__()
        self.url = "http://www.pingwest.com/subject/"
        self.item_path = "品玩->专题"  # 爬取网站的所在栏目
        self.relative_path = "PinWan/ZhuanTi/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.cookie_dict = {}
        self.content = ""

    def crawl(self):
        try:
            url = self.url
            while 1:
                content = self.get_req(url)
                bs_obj = BeautifulSoup(content, "html.parser")
                news_list = bs_obj.find("div", class_="subject-list").findAll("subject-item")
                for link in news_list:
                    try:
                        url_con = link.find("h2").find("a").get("href")
                        self.content = link.find("p", class_="info").get_text()
                        self.get_link_data(url_con)
                    except:
                        pass
                url = bs_obj.find("a", class_="next page-numbers")
                if not url:
                    break
                else:
                    url = url.get("href")
        except BaseException as e:
            logging.error("Get link error. URL=%s, errormsg = %s" % (url, str(e)))

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "html.parser")
            title = bs_obj.title.get_text()
            page_view = 0
            publish_time = "2000-01-01 00:00:00"
            return self.content, title, page_view, publish_time
        except BaseException as e:
            logging.error("Parse HTML error. ErrorMsg: %s" % str(e))
            raise BaseException()


class HeiJing(Crawler):

    def __init__(self):
        super().__init__()
        self.url = "http://www.pingwest.com/category/blackmirror/"
        self.item_path = "品玩->黑镜"  # 爬取网站的所在栏目
        self.relative_path = "PinWan/HeiJing/"
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.cookie_dict = {}

    def crawl(self):
        try:
            url = self.url
            while 1:
                content = self.get_req(url)
                bs_obj = BeautifulSoup(content, "html.parser")
                news_list = bs_obj.find("div", class_="black-list").findAll("div", class_="title")
                for link in news_list:
                    try:
                        url_con = link.find("a").get("href")
                        self.get_link_data(url_con)
                    except:
                        pass
                url = bs_obj.find("a", class_="next page-numbers")
                if not url:
                    break
                else:
                    url = url.get("href")
        except BaseException as e:
            logging.error("Get link error. URL=%s, errormsg = %s" % (url, str(e)))

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "html.parser")
            title = bs_obj.title.get_text()
            publish_time = Util.all_strip(bs_obj.find("span", class_="post-time").get_text())
            if "天" in publish_time:
                pos = publish_time.index("天")
                days = datetime.timedelta(int(publish_time[:pos]))
                publish_time = (datetime.datetime.now() - days).strftime(self.date_format)
            elif "小时" in publish_time:
                pos = publish_time.index("小")
                days = datetime.timedelta(int(publish_time[:pos]) // 24 + 1)
                publish_time = (datetime.datetime.now() - days).strftime(self.date_format)
            else:
                date_format = "%Y-%m-%d"
                publish_time = datetime.datetime.strptime(publish_time, date_format).strftime(self.date_format)
            page_view = 0
            content_tag = bs_obj.find("div", id="sc-container")
            post_footer = content_tag.find("p", class_="post-footer-wx")    # 删除不需要的内容
            if post_footer:
                post_footer.extract()
            block_quote = content_tag.find("blockquote")                     # 删除不需要的内容
            if block_quote:
                block_quote.extract()
            body_content = Util.get_content_from_tag(content_tag)
            return body_content, title, page_view, publish_time
        except BaseException as e:
            logging.error("Parse HTML error. ErrorMsg: %s" % str(e))
            raise BaseException()