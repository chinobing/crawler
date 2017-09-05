# coding=utf-8

import datetime
import re
import logging

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
        coding = "gb2312"
        date_format = "%Y-%m-%d"
        date_start = datetime.datetime.strptime("2015-06-01", date_format)
        date_end = datetime.datetime.now()
        date_dlt = datetime.timedelta(days=1)
        pattern = re.compile("(http://.*?)\"")
        while 1:
            date_dif = date_end - date_start
            if date_dif.days < 0:
                break
            url = self.url.format(date_start.strftime(date_format))
            content = self.get_req(url).decode(coding)
            link_list = pattern.findall(content)
            for link in link_list:
                self.get_link_data(link)
            date_start += date_dlt


