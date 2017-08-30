import requests
from bs4 import BeautifulSoup
import re
from ..Host import Host
from ..database import *

start_url = "https://www.huxiu.com/"
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
    pattern = re.compile(r'(http(s)?://www.aliresearch.com)?(/blog/article/detail/id/.*?html)')
    url = "/blog/article/detail/id/123.html"
    mathcr = pattern.match(url)
    print(mathcr.group())


# 阿里研究院的文章html是按规律排的,最开始的一个是11184, 然后到目前的23700左右.
# 这一类是 http://www.aliresearch.com/blog/article/detail/id/11184.html
# 阿里的地址是连续的.
url = 'http://www.aliresearch.com/blog/article/id/{}.html'


def save_simple_url():
    start = 11184
    last = 21372
    while start <= last:
        url_new = str.format(url, str(start))
        sql = "insert into ali_link(link, visit) VALUES(\"{}\", 0)"
        insert_data(sql.format(url_new))
        start += 1


class ALi(Host):
    def __init__(self):
        super().__init__()
        self.web_name = "hu_xiu"
        self.table_name = "huxiu_link"
        self.start_url = "https://www.huxiu.com"
        self.pattern = re.compile(r'(http(s)?://www.huxiu.com)?(/article/.*?html)')
        self.host_pattern = re.compile(r'https://www.huxiu.com')
        self.dir_path = "./huxiu/"

    def get_web_name(self):
        return self.web_name

    def get_content(self, bs_obj):
        try:
            content = bs_obj.find('p').find_next('p').get_text()[0: 50]
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

    def host_match(self, url):
        return self.host_pattern.match(url)

    def save_html(self, content, url):
        pos = self.get_last_slash_pos(url)
        path = self.dir_path + url[(pos + 1):]
        self.write(path, content)


