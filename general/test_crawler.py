import requests
import re
from bs4 import BeautifulSoup


def get_fisrt_page(start_url):
    r = requests.get(start_url)
    bs_obj = BeautifulSoup(r.content, "lxml")
    links = bs_obj.find_all('a')
    for link in links:
        print(link.get('href'))


def get_content_page(content_url):
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


def test_pattern(start_url, url):
    pattern = re.compile(r'(http(s)?://www.aliresearch.com)?(/blog/article/detail/id/.*?html)')
    matcher = pattern.match(url)
    if matcher:
        print(start_url + matcher.group(3))