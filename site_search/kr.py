# coding=utf-8

import requests
from copy import deepcopy


class KrSearch(object):

    kr_article_page_format = "http://36kr.com/search/articles/{}"  # 此处用汉字来做url的地址,但是不要quote
    kr_newsflashes_page_format = "http://36kr.com/search/newsflashes/{}"   # 快讯, 针对快讯不是网页,只是很多消息综合

    @staticmethod
    def search_article(keyword, search_page=5):
        pass

