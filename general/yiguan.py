import requests
from bs4 import BeautifulSoup
import re
from .Host import Host

start_url = 'http://www.199it.com'
content_url = 'http://www.199it.com/archives/623104.html'


def get_fisrt_page():
    r = requests.get(start_url)
    bs_obj = BeautifulSoup(r.content, "lxml")
    links = bs_obj.find_all('a')
    for link in links:
        print(link.get('href'))


def get_content_page():
    r = requests.get(content_url)
    bs_obj = BeautifulSoup(r.content, 'lxml')
    content = bs_obj.find('div', class_="entry-content")
    print(content.get_text()[0: 50])
    links = bs_obj.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            pattern(href)
    # print(bs_obj.title.text)


def pattern(url):
    pattern = re.compile(r'(http(s)?://www.199it.com)?(/archives/.*?html)')
    matcher = pattern.match(url)
    if matcher:
        print(start_url + matcher.group(3))

if __name__ == "__main__":
    # 可以解析到所有的关联文章的URL，由此开始进行爬取数据
    get_content_page()


# 易观国际的也是需要自己分析再爬数据,有些麻烦.
class YiGuan(Host):
    def __init__(self):
        super().__init__()
        self.web_name = "YiGuanGuoJi"
        self.table_name = "yiguan_link"
        self.start_url = 'http://www.199it.com'
        self.pattern = re.compile(r'(http(s)?://www.199it.com)?(/archives/.*?html)')
        self.path = "./yiguanguoji/"

    def get_web_name(self):
        return self.web_name

    def get_content(self, bs_obj):
        try:
            content = bs_obj.find('div', class_="entry-content").get_text()[0: 50]
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

    def save_html(self, content, url):
        pos = self.get_last_slash_pos(url)
        path = self.path + url[(pos + 1):]
        self.write(content, path)
