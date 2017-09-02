import requests
from bs4 import BeautifulSoup


def get_link():
    url = "http://www.jiemian.com/article/1594492.html"
    r = requests.get(url)
    print(r.text)
    bs_obj = BeautifulSoup(r.content, "lxml")
    bs_obj.find("div", class_="main-container")
    # print(bs_obj.text)


get_link()