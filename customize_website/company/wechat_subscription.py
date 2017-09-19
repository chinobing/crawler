# coding=utf-8

import logging
from bs4 import BeautifulSoup
import datetime
import time
import html

from customize_website.Crawler import Crawler
from customize_website.Util import Util
from customize_website.database import DBUtil


def main(run):
    if run:
        ws = WeChatSubscription()
        ws.crawl()


class WeChatSubscription(Crawler):
    wechat_sql = "update article_wechat set publish_time = '{}', html_path = '{}' where link = '{}'"

    """
    公众号爬虫,对每一个公众号爬完后开始爬另一个公众号.
    对于目前的设定,公众号保存结果中publish_time为空则表示没有访问过,否则已经访问过,不再爬取.
    """
    def __init__(self):
        super().__init__()
        self.url = "http://www.pingwest.com/category/figure/"
        self.relative_path = "WeXin/{}/"    # 公众号名称作为目录
        self.cookie_dict = {}
        self.id = None

    def set_first_id(self):
        sql = "select id from article_wechat_map limit 1"
        result = DBUtil.select_data(sql)
        if result:
            self.id = int(result['id'])
        else:
            self.id = 1

    def get_wechat_biz(self):
        sql = "select biz, wechat from article_wechat_map where id = {}".format(str(self.id))
        result = DBUtil.select_data(sql)
        if result:
            self.id += 1
            self.relative_path = self.relative_path.format(result['wechat'].replace("\"", "").replace(" ", ""))
            self.dirs = Crawler.all_file_dir + self.relative_path
            return result['biz'].replace("\"", "").replace(" ", "")
        else:
            return "", ""

    def get_all_wechat_link(self):
        biz = self.get_wechat_biz()
        sql = "select link from article_wechat where biz='{}'".format(biz)
        result = DBUtil.select_datas(sql)
        if result:
            return result
        else:
            return []

    def crawl(self):
        self.set_first_id()
        try:
            while 1:
                link_list = self.get_all_wechat_link()
                if len(link_list) == 0:
                    break
                for link in link_list:
                    self.get_link_data(link['link'])
        except BaseException as e:
            logging.error("Get link error, errormsg = %s" % str(e))

    def get_link_data(self, url):
        sql = "select publish_time from article_wechat WHERE link = '{}'".format(url)
        result = DBUtil.select_data(sql)
        if not result or result['publish_time']:
            return
        file_name = str(time.time())
        html_content = self.get_req(url)
        self.make_dirs()
        try:
            src_content = html_content.decode("utf-8")
        except:
            try:
                src_content = html_content.decode("gbk")
            except:
                logging.error("Can't decode with utf-8 or gbk")
                raise BaseException()
        self.save_html_file(content=src_content, file_name=file_name)
        body_content, publish_time = self.parse_html(src_content)
        self.save_content_file(content=body_content, file_name=file_name)
        self.insert_data_re(url, self.relative_path + file_name + ".html", publish_time)

    @staticmethod
    def insert_data_re(link, html_path, publish_time):
        sql = WeChatSubscription.wechat_sql.format(publish_time, html_path, link)
        DBUtil.update_data(sql)         # 更新数据

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "html.parser")
            publish_time = Util.all_strip(bs_obj.find("em", id="post-date").get_text())
            date_format = "%Y-%m-%d"
            publish_time = datetime.datetime.strptime(publish_time, date_format).strftime(self.date_format)
            content_tag = bs_obj.find("div", class_="rich_media_content ")
            body_content = Util.get_content_from_tag(content_tag)
            return body_content, publish_time
        except BaseException as e:
            logging.error("Parse HTML error. ErrorMsg: %s" % str(e))
            raise BaseException()
