# coding=utf-8

from bs4 import BeautifulSoup
import logging
from datetime import datetime

from customize_website.Crawler import Crawler
from customize_website.Util import Util


def main(run):
    if run:
        dssj = WenZhangKu_DianShangShuJu()
        dssj.crawl()


class WenZhangKu_DianShangShuJu(Crawler):

    def __init__(self):
        super().__init__()
        self.item_path = "互联网分析沙龙->文章库->电商数据"
        self.relative_path = 'HuLianWangFenXiShaLong/WenZhangKu/DianShangShuJu'
        self.dirs = Crawler.all_file_dir + self.relative_path
        self.url = "http://www.techxue.com/ecdata/"
        self.main_page_url = "http://www.techxue.com/"

    def crawl(self):
        try:
            url = self.url
            while 1:
                content = self.get_req(url)
                bs_obj = BeautifulSoup(content, "html.parser")
                # 从此页面中获取的都是相对地址,需要转化为绝对地址
                links = bs_obj.findAll("h3")
                for link in links:
                    href = link.find("a").get("href")
                    try:
                        self.get_link_data(self.main_page_url + href)
                    except:
                        pass
                next_page = bs_obj.find("a", class_="nxt")
                if not next_page:
                    break
                else:
                    url = next_page.get("href")   # 此处给出的地址是绝对地址
        except BaseException as e:
            logging.error("Crawl %s error. ErrorMsg: %s" % (url, str(e)))

    def parse_html(self, content):
        try:
            bs_obj = BeautifulSoup(content, "html.parser")
            publish_time = bs_obj.find("div", style="margin-top:15px;")  # 找到的可能不止一个,目前第一个位置是,网站改版可能会变化
            if publish_time:
                try:
                    # 时间很麻烦,可能会有汉字在其中,导致格式化错误.
                    publish_time = Util.all_strip(publish_time.get_text())
                    date_format = "%Y-%m-%d%H:%M"
                    publish_time = datetime.strptime(publish_time, date_format).strftime(self.date_format)
                except BaseException as e:
                    logging.warning("Parse time error. ErrorMsg: %s" % str(e))
            else:
                publish_time = "2000-01-01 00:00:00"
            title = bs_obj.title.get_text()
            content_tag = bs_obj.find("div", class_="nr")
            body_content = Util.get_content_from_tag(content_tag)
            page_view = 0
            return body_content, title, page_view, publish_time
        except BaseException as e:
            logging.error("Parse HTML error. ErrorMsg: %s" % (str(e)))

