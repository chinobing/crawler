import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import signal
import re
from .database import *

# 爬取36氪的数据,(爬取整个网站, 网站的的标题以及部分内容,给出链接).

sql_start = 'CREATE TABLE IF NOT EXISTS 36kr_link(id INT PRIMARY KEY AUTO_INCREMENT, link VARCHAR(1000), visit INT);'
col_link = 'link'
col_visit = 'visit'

start_url = "http://36kr.com"
urls = []  # 广度优先策略. 保存还未访问的网站
already_visit = []  # 保存已经访问的站点, 避免重复访问
data_format = "{},\t {},\t {}\r\n"
table_name = '36kr_link'
link_pattern = re.compile(r'(http(s)?://36kr\.com)?(/p/.*?html)')


def store_data(link, title, content):
    print(link)
    """
    保存爬取的数据到文件中
    :param link: 爬取的网页的URL
    :param title: 网页给出的title
    :param content: 长度限制在50字以内 
    :return: 
    """
    f = open('result.csv', 'at')
    f.write(str.format(data_format, title, content, link).replace("\n", ""))
    f.close()


def crawl(url):
    try:
        r = requests.get(url)
        content = r.content
        if content is None:
            return None
        bs_obj = BeautifulSoup(r.content)
        title = bs_obj.title
        body_text = bs_obj.find('section', class_='textblock')
        view_text = body_text[0: 100]
        store_data(url, title=title, content=view_text)
        already_visit.append(url)
        url_list = bs_obj.find_all('a', href=re.compile("http[s]://36kr.com/p"))
        urls.append(url_list)
    except Exception:
        pass


def handler(signum, frame):
    raise Exception("timeout")


def get_data(url):
    try:
        driver = webdriver.PhantomJS(executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        # 设置定时处理,超过120s没有返回数据则视为无法获得,抛出异常即可.
        signal.signal(signal.SIGALRM, handler)
        # 定时开始,
        signal.alarm(120)
        driver.get(url)
        # 取消定时 如果成功获取到页面.
        signal.alarm(0)
        # urls.remove(url)
        # already_visit.append(url)
        lists = driver.find_elements_by_tag_name('a')
        title = driver.title
        try:
            content = driver.find_element_by_tag_name('p').text[0: 50]
        except Exception as e:
            content = ""
        store_data(url, title, content)
        update_url(url)
        for node in lists:
            link = node.get_attribute('href')
            if link is None:
                continue
            match = link_pattern.match(link)
            if match:
                link = start_url + match.group(3)
                result = select_url(link)
                if result is None:
                    insert_url(link)
                # elif result['visit'] == 0:
                #     update_url(url)
                # if link not in already_visit:
                #     urls.append(link)
    except Exception as e:
        print(e)
    finally:
        driver.quit()

# 插入链接到数据库中
def insert_url(url):
    sql = str.format('INSERT INTO {}({}, {}) VALUES (\'{}\', {})', table_name, col_link, col_visit, url, 0)
    insert_data(sql)


# 查询链接是否已经被访问,返回的结果为空或者visit字段为0, 表示未被访问
def select_url(url):
    sql = str.format('SELECT * FROM {} WHERE link=\'{}\'', table_name, url)
    return select(sql)


# 更新现在正在被访问的链接.
def update_url(url):
    sql = str.format("UPDATE {} SET visit=1 WHERE link='{}'", table_name, url)
    insert_data(sql)


def select_top():
    sql = str.format('SELECT link FROM {} WHERE visit=0 LIMIT 10', table_name)
    return select_top_ten(sql)


def crawl_data():
    # 第一次运行时需要将start url加入到未访问数据库中,以此开始整个网站的爬取.
    # insert_url(start_url)
    while 1:
        links = select_top()
        for link in links:
            try:
                get_data(link['link'])
            except Exception as e:
                print(e)
