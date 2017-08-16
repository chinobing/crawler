import requests
from bs4 import BeautifulSoup
import re

start_url = 'http://www.199it.com/'
content_url = 'http://www.199it.com//archives/623104.html'


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