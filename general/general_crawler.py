import requests
from bs4 import BeautifulSoup
import time
import signal
from .database import *


class GeneralCrawler(object):

    save_data_format = "{},\t{},\t{}\r"
    insert_data_format = 'INSERT INTO {}(link, visit) VALUES (\'{}\', {})'
    update_date_format = "UPDATE {} SET visit=1 WHERE link='{}'"
    select_data_format = "SELECT * FROM {} WHERE link=\'{}\'"
    select__top_data_format = "SELECT link FROM {} WHERE visit=0 LIMIT 10"

    def __init__(self, host):
        self.host = host

    def save_data(self, link, title, content):
        f = open(self.host.get_web_name() + ".csv", 'at')
        f.write(str.format(GeneralCrawler.save_data_format, title, content, link).replace("\n", ""))

    # 爬取指定url的页面内容, 保存页面中该网站的链接
    def get_data(self, url):
        def handler(signum, frame):
            raise Exception("timeout")
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(120)
            r = requests.get(url)
            signal.alarm(0)
            bs_obj = BeautifulSoup(r.content)
            title = bs_obj.title.text
            content = self.host.get_content(bs_obj)
            self.save_data(link=url, title=title, content=content)
            self.update_url(url)
            lists = bs_obj.find_all('a')
            for link in lists:
                href = link.get_attribute('href')
                if href is None:
                    continue
                mather = self.host.match(href)
                if mather:
                    parse_url = self.host.get_parse_url(mather)
                    is_visited = self.select_url(parse_url)
                    if not is_visited:
                        self.insert_url(parse_url)
        except Exception as e:
            print(e)
        finally:
            # 资源清理
            pass

    def update_url(self, url):
        sql = str.format(GeneralCrawler.update_date_format, self.host.get_table_name(), url)
        insert_data(sql)

    def insert_url(self, url):
        sql = str.format(GeneralCrawler.insert_data_format, self.host.get_table_name(), url)
        insert_data(sql)

    def select_url(self, url):
        sql = str.format(GeneralCrawler.select_data_format, self.host.get_table_name(), url)
        return select(sql)

    def select_top(self):
        sql = str.format(GeneralCrawler.select__top_data_format, self.host.get_table_name())
        # 返回的结果是一个字典
        return select_top_ten(sql)

    def crawl(self):
        visited_start = self.select_url(self.host.get_start_url())
        if not visited_start:
            self.get_data(self.host.get_start_url())
        while 1:
            links = self.select_top()
            for link in links:
                # 避免异常中断爬取过程
                try:
                    self.get_data(link['link'])
                except Exception as e:
                    print(e)