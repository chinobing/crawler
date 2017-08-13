import urllib
from urllib import parse
from .header import *
from .parser import Parser
from lxml import etree
from .lagouspider import get_content
from .lagouspider import search_url
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import re


url = "https://easy.lagou.com/search/result.json?pageNo={}&keyword={}&city=%E4%B8%8D%E9%99%90"

def gzip_test():
    url = 'https://easy.lagou.com/search/resume/2c16b0796130d164108065be17938906.htm?outerPositionId='
    data = get_content(url, headers)
    html = etree.HTML(data.decode('utf-8'))
    parses = Parser(html, url)
    parses.parse()
    print(parses.user_info.to_string())


def get_last_page(page_no, key_word):
    try:
        key_word = quote(key_word)
        url_new = str.format(search_url, page_no, key_word)
        # request1 = urllib.request.Request(url_new, headers=headers)
        # response = urllib.request.urlopen(request1)
        # data = response.read()
        data = get_content(url_new, headers)
        html = etree.HTML(data.decode('utf-8'))
        last_page = html.xpath('//a/@data-page')
        return int(last_page[last_page.__len__() - 1])
    except Exception as e:
        return -1


def phantom_and_selenium():
    desired_capa = DesiredCapabilities.PHANTOMJS.copy()
    PHANTOM_PRIFIX = 'phantomjs.page.customHeader.'
    keys = headers.keys()
    for key in keys:
        if key != "Cookie":
            desired_capa[PHANTOM_PRIFIX + key] = headers.get(key)
    # # desired_capa['phantomjs.page.customHeader.User-Agent'] = ''
    driver = webdriver.PhantomJS(executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.add_cookie(get_cookie())
    driver.get("https://passport.lagou.com/login/login.html")
    driver.close()


def get_cookie():
    cookies = {}
    cookie_strs = headers["Cookie"].split(';')
    for cookie_str in cookie_strs:
        strs = cookie_str.split('=', maxsplit=1)
        cookies[strs[0].strip()] = strs[1].strip()
    return cookies


def get_out_of_page():
    try:
        url_new = url.format(100000, parse.quote("德勤"))
        # request1 = urllib.request.Request(url_new, headers=headers_json)
        # response = urllib.request.urlopen(request1)
        # data = response.read()
        data = get_content(url_new, headers_json)
        patern = re.compile('\"resumeKey\":\"([a-z0-9]{32})\"')
        url_list = patern.findall(data.decode('utf-8'))
        return url_list
    except Exception as e:
        return []