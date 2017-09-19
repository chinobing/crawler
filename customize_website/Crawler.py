# coding=utf-8
import os
import logging
import requests
from .database import DBUtil
import html
import time
import html
from selenium import webdriver
from copy import deepcopy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Crawler(object):

    all_file_dir = "/home/jfq/Documents/datapro_html/"

    select_sql_format = "SELECT * FROM article_link WHERE link = \"{}\""
    insert_sql_format = "INSERT INTO article_link(link, item_path, title, html_path," \
                        " page_view, publish_time) VALUES(\"{}\", \"{}\", \"{}\", \"{}\"," \
                        "{}, \"{}\")"

    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 修改userAgent 以及不加载图片
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")  # 设置user-agent请求头
    dcap["phantomjs.page.settings.loadImages"] = False

    cookie_dict = {
        "name": None,
        "value": None,
        "domain": None,
        "path": "/",
        # "expire": None
    }

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
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.cookie_count = 0

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
        try:
            # 首先查询目标链接是否已经在数据库中,如果在,则返回.
            select_sql = Crawler.select_sql_format.format(url)
            result = DBUtil.select_data(select_sql)
            if result:
                return
            slash_pos = -1
            if url.endswith("/"):
                url = url[:len(url) - 1]
            while 1:
                tmp = url.find("/", slash_pos + 1)
                if tmp < 0:
                    break
                slash_pos = tmp
            point_pos = url.find(".", slash_pos)
            if point_pos > 0:
                file_name = url[slash_pos + 1: point_pos]
            else:
                file_name = url[slash_pos + 1:]
            html_content = self.use_phantom_get_req(url, "36kr.com")
            self.make_dirs()
            src_content = html_content
            # try:
            #     src_content = html_content.decode("utf-8")
            # except:
            #     try:
            #         src_content = html_content.decode("gbk")
            #     except:
            #         logging.error("Can't decode with utf-8 or gbk")
            #         raise BaseException()
            self.save_html_file(content=src_content, file_name=file_name)
            body_content, title, page_view, publish_time = self.parse_html(src_content)
            self.save_content_file(content=body_content, file_name=file_name)
            self.insert_data(url, self.item_path, html.escape(title),
                             self.relative_path + file_name + ".html",
                             page_view, publish_time)
            # time.sleep(0.5)
        except BaseException as e:
            logging.error("Process link failed. URL=%s, ErrorMsg: %s" % (url, str(e)))
            raise BaseException

    @staticmethod
    def insert_data(link, item_path, title, html_path, page_view, publish_time):
        try:
            insert_sql = Crawler.insert_sql_format.format(link, item_path, html.escape(title),
                                                          html_path, page_view, publish_time)
            DBUtil.insert_data(insert_sql)
        except:
            raise BaseException()

    def parse_html(self, content):
        """
        :return: 链接所在的正文, 转义所有的换行符为\n
        """
        return "", "", 0, "2000:01:01 00:00:00"

    def make_dirs(self):
        try:
            if not os.path.isdir(self.dirs):
                os.makedirs(self.dirs)
        except BaseException as e:
            logging.error("Make directory error. ErrorMsg: %s" % str(e))
            raise BaseException()

    def save_html_file(self, file_name, content):
        try:
            self.save_file(self.dirs + file_name + ".html", content)
        except BaseException as e:
            logging.error("Save HTML file error. ErrorMsg: %s" % str(e))
            raise BaseException()

    def save_content_file(self, file_name, content):
        try:
            self.save_file(self.dirs + file_name + ".txt", content)
        except BaseException as e:
            logging.error("Save content file error. ErrorMsg: %s" % str(e))
            raise BaseException()

    @staticmethod
    def save_file(path, content):
        f = open(path, "wt", encoding="utf-8")
        f.writelines(content)
        f.close()

    def get_req(self, link):
        try:
            if self.cookie_count < 50:
                r = requests.get(link, cookies=self.cookie_dict, timeout=10)
                self.cookie_count += 1
            else:
                r = requests.get(link, timeout=10)
                self.cookie_count = 0
                self.cookie_dict = {}
        except requests.ConnectTimeout:
            logging.error("Read link connection timeout. URL=%s" % link)
            raise BaseException()
        try:
            if not self.cookie_dict:
                self.cookie_dict = requests.utils.dict_from_cookiejar(r.cookies)
            logging.info("Get %s success." % link)
            return r.content
        except BaseException as e:
            logging.error("Get URL content error. URL = " + link + " ErrorMsg: " + str(e))
            raise BaseException()

    def save_link(self, link):
        """
        先保存链接，后遍历链接再去内容。
        :return:
        """
        if self.match_link(link):
            self.insert_data(link=link, title="", html_path="",item_path=self.item_path,
                             page_view=0, publish_time="2000-01-01 00:00:00")
        else:
            logging.error("Get link is not this site.")
            raise BaseException()

    def match_link(self, link):
        pass

    def use_phantom_get_req(self, url, domain):
        try:
            driver = webdriver.PhantomJS(
                executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',
                desired_capabilities=Crawler.dcap)
            # keys = self.cookie_dict.keys()
            # for key in keys:
            #     cookie_dict_ins = deepcopy(Crawler.cookie_dict)
            #     cookie_dict_ins['name'] = key
            #     cookie_dict_ins['value'] = self.cookie_dict[key]
            #     cookie_dict_ins['domain'] = domain
            #     driver.add_cookie(cookie_dict_ins)
            driver.set_page_load_timeout(30)
            driver.get(url)
            # if len(self.cookie_dict) == 0:
            #     self.cookie_dict = driver.get_cookies()
            # self.cookie_count += 1
            # if self.cookie_count >= 50:
            #     self.cookie_count = 0
            #     self.cookie_dict = {}
            # 等待特定数据出现
            # driver.implicitly_wait(10)
            logging.info("Get %s success." % url)
            return driver.page_source
        except BaseException as e:
            logging.error("Get link error. ErrorMsg: %s" % str(e))
        finally:
            driver.quit()