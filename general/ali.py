import requests
from bs4 import BeautifulSoup
import re

start_url = "http://www.aliresearch.com/"
content_url = "http://www.aliresearch.com/Blog/Article/detail/id/20516.html".lower()


def get_fisrt_page():
    r = requests.get(start_url)
    bs_obj = BeautifulSoup(r.content, "lxml")
    links = bs_obj.find_all('a')
    for link in links:
        print(link.get('href'))


def get_content_page():
    r = requests.get(content_url)
    bs_obj = BeautifulSoup(r.content, 'lxml')
    content = bs_obj.find('p')
    content_next = content.find_next("p")
    print(content.get_text())
    print(content_next.get_text())

    links = bs_obj.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            test_pattern(href)
    # print(bs_obj.title.text)


def test_pattern(url):
    pattern = re.compile(r'(http(s)?://www.aliresearch.com)?(/blog/article/detail/id/.*?html)')
    matcher = pattern.match(url)
    if matcher:
        print(start_url + matcher.group(3))

if __name__ == "__main__":
    # 可以解析到所有的关联文章的URL，由此开始进行爬取数据
    get_content_page()


class ALi(object):
    def __init__(self):
        self.web_name = "alibaba-research"
        self.table_name = "ali_link"
        self.start_url = "http://www.aliresearch.com"
        self.pattern = re.compile(r'(http(s)?://www.aliresearch.com)?(/blog/article/detail/id/.*?html)')

    def get_web_name(self):
        return self.web_name

    def get_content(self, bs_obj):
        try:
            content = bs_obj.find('p').find_next('p').get_text()
        except Exception as e:
            content = ""
        return content

    def match(self, href):
        return self.pattern.match(href)

    def get_table_name(self):
        return self.table_name

    def get_start_url(self):
        return self.start_url

    def get_parse_url(self, matcher):
        return self.start_url + matcher.group(3)

