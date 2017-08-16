import requests
from bs4 import BeautifulSoup
import re

start_url = "https://www.mckinsey.com.cn"
content_url = "https://www.mckinsey.com.cn/%E4%B8%AD%E5%9B%BD%E8%B4%A2%E5%AF%8C%E7%AE%A1%E7%90%86%E8%A1%8C%E4%B8%9A%E8%BF%8E%E6%9D%A5%E6%B7%98%E9%87%91%E7%83%AD/"

def get_fisrt_page():
    r = requests.get(start_url)
    bs_obj = BeautifulSoup(r.content, "lxml")
    links = bs_obj.find_all('a')
    for link in links:
        print(link.get('href'))


def get_content_page():
    r = requests.get(content_url)
    bs_obj = BeautifulSoup(r.content, 'lxml')
    content = bs_obj.find('div', class_="post-content")
    print(content.get_text()[0: 50])
    links = bs_obj.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            pattern(href)
    # print(bs_obj.title.text)


def pattern(url):
    pattern = re.compile(r'(http(s)?://www.mckinsey.com.cn)?(/[^/]*)')
    matcher = pattern.match(url)
    if matcher:
        print(start_url + matcher.group(3))

if __name__ == "__main__":
    # 可以解析到所有的关联文章的URL，由此开始进行爬取数据
    get_content_page()