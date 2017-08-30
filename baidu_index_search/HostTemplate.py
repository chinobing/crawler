import datetime
import requests
import re
from general.database import *
from urllib.parse import quote
from lxml import etree
import time
import logging

class HostTemplate(object):
    one_day_delta = datetime.timedelta(days=1)
    insert_sql = "INSERT INTO {}(link, visit) VALUES('{}', 0)"
    select_sql = "SELECT * FROM {} WHERE link = '{}'"

    def __init__(self):
        self.table_name = None          # 当前爬取网站保存到数据库中的表名(str)
        self.site = None                # 当前爬取网站的站点地址,不需要网络类型(例如www)(str)
        self.cur_date = None            # 选择的开始爬的时间 (date)
        self.end_date = None            # 选择爬取结束时间 (date)
        self.date_format = None         # 时间的格式(yyyy-MM-dd) (str)
        self.pattern = None             # 对站点过滤的正则表达式 (re pattern)
        self.max_page = 10              # 用当前时间搜索后,最多在百度上访问几页
        self.cookies_dict = None
        self.count = 0

    def get_next_day(self):
        """
        获取后一天的日期,
        :param date: 当前日期
        :return: 
        """
        self.cur_date += HostTemplate.one_day_delta

    def get_date_str(self, date):
        return date.strftime(self.date_format)

    def insert_url(self, url):
        sql = HostTemplate.insert_sql.format(self.table_name, url)
        insert_data(sql)

    def select_url(self, url):
        sql = HostTemplate.select_sql.format(self.table_name, url)
        # 如果查询的值不存在则返回空字典
        return select(sql)

    def pattern_match(self, url):
        return ''

    @staticmethod
    def parse_baidu_link(url):
        """
        从百度的链接中得到目标网页的链接.
        :param url: 百度的url
        :return: 
        """
        try:
            r = requests.get(url, allow_redirects=False)
            location = r.headers["Location"]
        except Exception as e:
            location = ""
        return location

    # 用当前日期做关键字,保存得到的链接
    def get_link_from_baidu(self):
        key_word_quote = quote(self.get_date_str(self.cur_date))
        url = str.format('http://www.baidu.com/s?ie=UTF-8&wd={}%20site%3A{}', key_word_quote, self.site)
        failure = 0
        max_page = self.max_page
        # url用来控是否有下一页, failure 用来控制失败次数
        while len(url) > 0 and failure < 10:
            # print(url)
            logging.info(url)
            try:
                if self.cookies_dict is None or self.count >= 50:
                    r = requests.get(url, timeout=10)
                    self.cookies_dict = requests.utils.dict_from_cookiejar(r.cookies)
                    self.count = 0
                else:
                    r = requests.get(url, cookies=self.cookies_dict, timeout=10)
            except Exception as e:
                self.cookies_dict = None
                failure += 1
                continue

            if r.status_code == 200:
                hrefs = list(set(re.findall('"(http://www\\.baidu\\.com/link\\?url=.*?)"', r.content.decode('utf-8'))))
                for href in hrefs:
                    # time.sleep(1)
                    # 将百度的链接转换为目标链接
                    target_url = HostTemplate.parse_baidu_link(href)
                    # 如果目标链接符合过滤规则, 同时目标链接不在数据库中, 将目标链接保存到数据库中
                    format_url = self.pattern_match(target_url)
                    if len(format_url) > 0 and not self.select_url(format_url):
                        self.insert_url(format_url)
                    # if len(self.pattern_match(target_url)) > 0 and not self.select_url(target_url):
                    #     self.insert_url(target_url)

                tree = etree.HTML(r.content)
                # 获取百度的下一页的地址(在百度页面中看到的下一页就是)
                next_page_text = tree.xpath(
                    '//div[@id="page"]/a[@class="n" and contains(text(), "下一页")]/@href')
                # 如果没有下一页标签,则说明访问完了
                url = 'http://www.baidu.com' + next_page_text[0].strip() if next_page_text else ''
                failure = 0
                max_page -= 1
                if max_page <= 0:
                    break
            else:
                failure += 2
                print('search failed: %s' % r.status_code)
        if failure >= 10:
            print('search failed: %s' % url)

    @staticmethod
    def compare_date(date_cur, date_target):
        """
        如果data_cur所在的时间在date_target之后,则放回true,
        否则返回false
        :param date_cur: 
        :param date_target: 
        :return: 
        """
        day_dif = date_cur - date_target
        if day_dif.days > 0:
            return 1
        else:
            return 0

    def crawl_link(self):
        logging.basicConfig(level=logging.INFO,
                            format=("%(asctime)s %(levelname)s %(message)s"),
                            datefmt="%Y-%m-%d %H:%M:%S",
                            filename="log/" + self.table_name + ".log",
                            filemode="a",
                            )
        # 如果表不存在则创建表
        create_table(self.table_name)
        while HostTemplate.compare_date(self.end_date, self.cur_date):
            try:
                self.get_link_from_baidu()
                self.get_next_day()
                time.sleep(3)
            except Exception as e:
                print(e)

