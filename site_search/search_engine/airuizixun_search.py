# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import requests


class AiRuiZiXunSearch(object):
    """
    利用艾瑞网搜索得到的文章的结果.艾瑞网搜索的结果会分成多个板块,目前的处理方式是针对多个板块分别取数据,然后综合在一起.
    但是有的板块在一页放不下,这个问题目前还没有解决.目前仅仅只提取艾瑞咨询的搜索页面的消息,不能下一页.
    """

    search_url = "http://s.iresearch.cn/search/{}/"

    item = {"title": None, "abstract": None, "link": None, "date": ""}

    @staticmethod
    def search(key_word, search_page=5):
        """
        利用关键字进行搜索, 搜索结果返回指定页数,
        :param key_word: 关键字.
        :param search_page: 需要返回几页结果.
        :return: 返回字典, {} 
        """
        result_list = {"result_list": []}
        max_page = search_page
        try:
            key_word_quote = parse.quote(key_word)
            url = AiRuiZiXunSearch.search_url.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    search_items = bs_obj.find("div", class_="m-search-resu").findAll("div", class_="m-bd")
                    for search_item in search_items:
                        result_links = search_item.findAll("li")
                        for result in result_links:
                            try:
                                item_ins = deepcopy(AiRuiZiXunSearch.item)
                                item_ins['link'] = result.find("a").get("href")
                                item_ins['title'] = result.find("a").get_text()
                                item_ins['abstract'] = ""  # 艾瑞咨询的搜索结果没有摘要
                                item_ins["date"] = result.find("span", class_="time").get_text()
                                result_list["result_list"].append(item_ins)
                            except BaseException as e:
                                logging.error("Parse AiRuiZiXun result error. ErrorMsg: %s" % str(e))
                    break  # 访问一次后即可停止.
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get AiRuiZiXun search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def search_page(key_word, page):
        """
        get specified page in AiRuiZiXun. AiRuiZiXun 并没有取特定的页,他有多个模块,如果要写就要写每个模块的.
        :param key_word: 
        :param page: 
        :return: 
        """
        result_list = {"result_list": []}
        try:
            key_word_quote = parse.quote(key_word)
            url = AiRuiZiXunSearch.search_url.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    search_items = bs_obj.find("div", class_="m-search-resu").findAll("div", class_="m-bd")
                    for search_item in search_items:
                        result_links = search_item.findAll("li")
                        for result in result_links:
                            try:
                                item_ins = deepcopy(AiRuiZiXunSearch.item)
                                item_ins['link'] = result.find("a").get("href")
                                item_ins['title'] = result.find("a").get_text()
                                item_ins['abstract'] = ""  # 艾瑞咨询的搜索结果没有摘要
                                item_ins["date"] = result.find("span", class_="time").get_text()
                                result_list["result_list"].append(item_ins)
                            except BaseException as e:
                                logging.error("Parse AiRuiZiXun result error. ErrorMsg: %s" % str(e))
                    break  # 访问一次后即可停止.
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get AiRuiZiXun search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    url_list = AiRuiZiXunSearch.search("区块链", search_page=1)    # 已经测试过了,运行正常
    print(url_list["result_list"])
