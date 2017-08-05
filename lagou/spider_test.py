import urllib
from urllib import request
from .header import *
from .parser import Parser
from lxml import etree
from .lagouspider import get_content


def gzip_test():
    url = 'https://easy.lagou.com/search/resume/2c16b0796130d164108065be17938906.htm?outerPositionId='
    data = get_content(url, headers)
    html = etree.HTML(data.decode('utf-8'))
    parses = Parser(html, url)
    parses.parse()
    print(parses.user_info.to_string())
