# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import requests
import json
import time


class HuaErJieJianWenSearch(object):
    """
    利用华尔街见闻的API调用搜索得到的文章的结果.
    """

    news_search_url = "https://api-prod.wallstreetcn.com/apiv1/search/article?query={}&order_type=time&cursor={}&limit=20"

    live_news_search_url = "https://wallstreetcn.com/search?q={}&tab=live"

    site_url = "https://wallstreetcn.com"

    item = {"title": None, "abstract": None, "link": None, "date": ""}

    @staticmethod
    def news_search(key_word, search_page=5):
        """
        利用关键字进行搜索, 搜索结果返回指定页数,
        :param key_word: 关键字.
        :param search_page: 需要返回几页结果.
        :return: 返回字典, {} 
        """
        result_list = {"result_list": []}
        max_page = search_page
        try:
            page = 1
            key_word_quote = parse.quote(key_word)
            url = HuaErJieJianWenSearch.news_search_url.format(key_word_quote, page)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    result_links = json.loads(r.content, encoding='utf-8')['data']['items']
                    for result in result_links:
                        try:
                            item_ins = deepcopy(HuaErJieJianWenSearch.item)
                            # title_node = result.find("div", class_="search-article-content")
                            item_ins['link'] = result['uri']
                            item_ins['title'] = result['title']
                            item_ins['abstract'] = result['content_short']
                            item_ins["date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result['display_time']))
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse LeiFeng result error. ErrorMsg: %s" % str(e))
                    page += 1
                    url = HuaErJieJianWenSearch.news_search_url.format(key_word_quote, page)
                    failure = 0
                    max_page -= 1
                    if max_page <= 0:
                        break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get HuaErJieJianWen search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def live_news_search(key_word, search_page=5):
        """
        搜索实时新闻的页面.得到的结果是没有链接与标题的,只有新闻的介绍.并且涉及到的条目数比较多.
        :param key_word: 关键字.
        :param search_page: 需要返回几页结果.
        :return: 返回字典, {} 
        """
        result_list = {"result_list": []}
        max_page = search_page
        try:
            key_word_quote = parse.quote(key_word)
            url = HuaErJieJianWenSearch.news_search_url.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result_links = bs_obj.findAll("div", class_="wwscn-search__live-item")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(HuaErJieJianWenSearch.item)
                            # title_node = result.find("div", class_="search-article-content")
                            item_ins['link'] = ""
                            item_ins['title'] = ""
                            item_ins['abstract'] = result.find("div", class_="live-content-text").get_text()
                            item_ins["date"] = result.find("div", class_="live-time").get_text()
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse LeiFeng result error. ErrorMsg: %s" % str(e))
                    next_page = bs_obj.find("a", class_="next")
                    if next_page:
                        url = next_page.get("href")
                    else:
                        url = ""
                    failure = 0
                    max_page -= 1
                    if max_page <= 0:
                        break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get LeiFeng search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def search(key_word, search_page=5):
        """
        利用关键字进行搜索,返回指定的结果.
        :param key_word: 
        :param search_page: 
        :return: 
        """
        return HuaErJieJianWenSearch.news_search(key_word, search_page)

    @staticmethod
    def search_page(key_word, page):
        """
        爬取特定的页面
        :param key_word: 
        :param search_page: 
        :return: 
        """
        result_list = {"result_list": []}
        try:
            key_word_quote = parse.quote(key_word)
            url = HuaErJieJianWenSearch.news_search_url.format(key_word_quote, page)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    result_links = json.loads(r.content, encoding='utf-8')['data']['items']
                    for result in result_links:
                        try:
                            item_ins = deepcopy(HuaErJieJianWenSearch.item)
                            # title_node = result.find("div", class_="search-article-content")
                            item_ins['link'] = result['uri']
                            item_ins['title'] = result['title']
                            item_ins['abstract'] = result['content_short']
                            item_ins["date"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                             time.localtime(result['display_time']))
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse LeiFeng result error. ErrorMsg: %s" % str(e))
                    break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get HuaErJieJianWen search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    url_list = HuaErJieJianWenSearch.search_page("资本", page=3)    # 已经测试过了,运行正常
    for t in url_list["result_list"]:
        print(t)
