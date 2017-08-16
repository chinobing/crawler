import requests
from lxml import etree
import urllib
from urllib.request import *

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Host': 'passport.lagou.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

def login(account, password):
    payload = {""}
    login_url = "https://passport.lagou.com/login/login.html"
    r = requests.get(login_url, headers=headers)
    html = etree.HTML(r.text)
    print(html.xpath("//title")[0].text)

if __name__ == "__main__":
    login("123", "234")