# coding=utf-8

import re
import logging
from bs4 import BeautifulSoup
import datetime
import time

from customize_website.Crawler import Crawler


def main():
    gdxn = ChuangYe_GunDongXinWen()
    gdxn.crawl()


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


