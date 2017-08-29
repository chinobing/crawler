import requests
from bs4 import BeautifulSoup
import time
import signal
from .database import *
from selenium import webdriver


class GeneralCrawler(object):
    save_data_format = "{},\t{},\t{}\r"
    insert_data_format = 'INSERT INTO {}(link, visit) VALUES (\'{}\', 0)'
    update_date_format = "UPDATE {} SET visit=1 WHERE link='{}'"
    select_data_format = "SELECT * FROM {} WHERE link=\'{}\'"
    select__top_data_format = "SELECT link FROM {} WHERE visit=0 LIMIT 10"

    def __init__(self, host):
        self.host = host

    def save_data(self, link, title, content):
        try:
            print(link)
            f = open(self.host.get_web_name() + ".csv", 'at')
            f.write(str.format(GeneralCrawler.save_data_format, title, content, link).replace("\n", ""))
        finally:
            f.close()

    # 爬取指定url的页面内容, 保存页面中该网站的链接
    def get_data(self, url):
        print(url)
        def handler(signum, frame):
            raise Exception("timeout")
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(120)
            r = requests.get(url)
            signal.alarm(0)
            bs_obj = BeautifulSoup(r.content, 'lxml')
            # if self.host.match(url):
                # title = bs_obj.title.text
                # content = self.host.get_content(bs_obj).replace("\n", "")
                # self.save_data(link=url, title=title, content=content)
                # self.host.save_html(url, r.content.decode('utf-8'))
            self.update_url(url)
            lists = bs_obj.find_all('a')
            for link in lists:
                href = link.get('href')
                if href is None:
                    continue
                mather = self.host.match(href)
                if mather:
                    parse_url = self.host.get_parse_url(mather)
                    is_visited = self.select_url(parse_url)
                    if not is_visited:
                        self.insert_url(parse_url)
                # 如果从主页进入无法遍历整个站点所有文章,则把相同host也加入到数据库中,尝试重新遍历
                # else:
                #     if self.host.host_match(href):
                #         is_visited = self.select_url(href)
                #         if not is_visited:
                #             self.insert_url(href)
        except Exception as e:
            print(e)
        finally:
            # 资源清理
            pass

    def get_data_use_phantomjs(self, url):
        print(url)
        def handler(signum, frame):
            raise Exception("timeout")

        try:
            driver = webdriver.PhantomJS(
                executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(120)
            driver.get(url)
            # 有每个网站自己这是相应的等待条件
            self.host.phantomjs_condition(driver)
            signal.alarm(0)
            # bs_obj = BeautifulSoup(driver.page_source.encode('utf-8'), 'lxml')
            # if self.host.match(url):
            # title = bs_obj.title.text
            # content = self.host.get_content(bs_obj).replace("\n", "")
            # self.save_data(link=url, title=title, content=content)
            # self.host.save_html(url, r.content.decode('utf-8'))
            self.update_url(url)
            lists = driver.find_elements_by_tag_name('a')
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
                        # 如果从主页进入无法遍历整个站点所有文章,则把相同host也加入到数据库中,尝试重新遍历
                        # else:
                        #     if self.host.host_match(href):
                        #         is_visited = self.select_url(href)
                        #         if not is_visited:
                        #             self.insert_url(href)
        except Exception as e:
            print(e)
        finally:
            # 资源清理
            driver.quit()

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

    def crawl(self, use_phantomjs):
        visited_start = self.select_url(self.host.get_start_url())
        if not visited_start:
            # self.get_data(self.host.get_start_url())
            self.insert_url(self.host.get_start_url())
        while 1:
            links = self.select_top()
            for link in links:
                # 避免异常中断爬取过程
                try:
                    if use_phantomjs:
                        # phantomjs耗时较长,可以不用沉睡2秒
                        self.get_data_use_phantomjs(link['link'])
                    else:
                        self.get_data(link['link'])
                        time.sleep(2)
                except Exception as e:
                    print(e)
