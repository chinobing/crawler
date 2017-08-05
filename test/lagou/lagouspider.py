# -*- coding:utf-8 -*-
import logging
import urllib
import re
import zlib
from urllib import request
from urllib import parse
import gzip
from io import StringIO
from lxml import etree
from .parser import Parser
import chardet
from .header import *
from .lagou_database import *

import time

url = "https://easy.lagou.com/search/result.json?pageNo={}&keyword={}&city=%E4%B8%8D%E9%99%90"
patern = re.compile('\"resumeKey\":\"([a-z0-9]{32})\"')
resume_url = "https://easy.lagou.com/search/resume/{}.htm?outerPositionId="
search_url = 'https://easy.lagou.com/search/result.htm?pageNo={}&keyword={}&city=%E4%B8%8D%E9%99%90'


def login():
    print('login')


def get_json_data(page_no, key_word):
    try:
        url_new = url.format(page_no, key_word)
        # request1 = urllib.request.Request(url_new, headers=headers_json)
        # response = urllib.request.urlopen(request1)
        # data = response.read()
        data = get_content(url_new, headers_json)
        # encoding = chardet.detect(data)
        url_list = patern.findall(data.decode('utf-8'))
        return url_list
    except Exception as e:
        return []


def get_last_page(page_no, key_word):
    try:
        url_new = str.format(search_url, page_no, key_word)
        # request1 = urllib.request.Request(url_new, headers=headers)
        # response = urllib.request.urlopen(request1)
        # data = response.read()
        data = get_content(url_new, headers)
        encoding = chardet.detect(data)
        html = etree.HTML(data.decode(encoding["encoding"]))
        last_page = html.xpath('//a/@data-page')
        return int(last_page[last_page.__len__() - 1])
    except Exception as e:
        return -1


def get_data(key_word, page_no_last):
    if page_no_last <= 0:
        return
    file = open(key_word + '.csv', 'wt', encoding='utf-8')
    key_word = urllib.parse.quote(key_word)
    count = 0
    for i in range(1, page_no_last + 1):
        resume_url_list = get_json_data(i, key_word)
        for resume_key in resume_url_list:
            if count % 30 == 0:
                time.sleep(60)
            try:
                query_result = select(resume_key)
                if query_result is not None:
                    continue
                else:
                    insert_data(resume_key)
                url_new = resume_url.format(resume_key)
                # request1 = urllib.request.Request(url_new, headers=headers)
                # response = urllib.request.urlopen(request1)
                # data = response.read()
                # # encoding = chardet.detect(data)
                data = get_content(url_new, headers)
                parses = Parser(etree.HTML(data.decode("utf-8")), resume_key)
                try:
                    parses.parse()
                except Exception as e:
                    print(url_new)
                    logging.exception(e)
                    continue
                file.writelines(parses.user_info.to_string() + '\n')
                count = count + 1
                print(count)
            except Exception as e:
                print(url_new)
                logging.exception(e)
    file.close()


def get_content(url, header):
    req = urllib.request.Request(url, headers=header)
    resp = urllib.request.urlopen(req)
    content = resp.read()
    encoding = resp.info().get("Content-Encoding")
    if encoding == 'gzip':
        content = gzip_dec(content)
    elif encoding == 'deflate':
        content = deflate(content)
    return content


def gzip_dec(data):
    return gzip.decompress(data)


def deflate(data):
    try:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)
