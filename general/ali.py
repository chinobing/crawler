import requests
from bs4 import BeautifulSoup

start_url = "http://www.aliresearch.com/"
content_url = "http://www.aliresearch.com/Blog/Article/detail/id/20516.html"


def get_fisrt_page():
    r = requests.get(start_url)
    bs_obj = BeautifulSoup(r.content, "lxml")
    links = bs_obj.find_all('a')
    for link in links:
        print(link.get('href'))


def get_content_page():
    r = requests.get(content_url)
    bs_obj = BeautifulSoup(r.content, 'lxml')
    links = bs_obj.find_all('a')
    for link in links:
        print(link.get('href'))
    print(bs_obj.title.text)


get_content_page()