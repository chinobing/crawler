# coding=utf-8

import requests
from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging


class ZhiHuSearch(object):
    """
    利用搜狗搜索得到的知乎的结果:知乎有一个可以利用搜狗的.
    """

    page_url = "http://zhihu.sogou.com/zhihu"  # 匹配parse过的关键词即可.

    search_url = "http://zhihu.sogou.com/zhihu?query={}"   # 此处需要加上web,因为下一页给出的地址只有参数

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
            url = ZhiHuSearch.search_url.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result_links = bs_obj.find("div", class_="box-result").findAll("div", class_="result-about-list")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(ZhiHuSearch.item)
                            title_node = result.find("h4")
                            item_ins['link'] = title_node.find("a").get("href")
                            item_ins['title'] = title_node.get_text()
                            item_ins['abstract'] = result.find("div", class_="about-text").find("p", class_="summary-answer-num").get_text()
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse 360 result error. ErrorMsg: %s" % str(e))
                    next_page = bs_obj.find("a", class_="np")
                    if next_page:
                        url = ZhiHuSearch.page_url + next_page.get("href")
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
            logging.error("Get ZhiHu search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def search_page(key_word, page):
        """
        利用关键字进行搜索, 搜索结果返回特定页数,
        :param key_word: 关键字.
        :param page: 返回第几页结果.
        :return: 返回字典, {} 
        """
        result_list = {"result_list": []}
        try:
            key_word_quote = parse.quote(key_word)
            url = ZhiHuSearch.search_url.format(key_word_quote)
            # url用来控是否有下一页, failure 用来控制失败次数
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                bs_obj = BeautifulSoup(r.content, "html.parser")
                url = ZhiHuSearch.page_url + bs_obj.find("a", class_="np").get("href").replace("page=2", "page=" + str(page))
                r = requests.get(url, timeout=10)
                bs_obj = BeautifulSoup(r.content, "html.parser")
                result_links = bs_obj.find("div", class_="box-result").findAll("div", class_="result-about-list")
                for result in result_links:
                    try:
                        item_ins = deepcopy(ZhiHuSearch.item)
                        title_node = result.find("h4")
                        item_ins['link'] = title_node.find("a").get("href")
                        item_ins['title'] = title_node.get_text()
                        item_ins['abstract'] = result.find("div", class_="about-text").find("p", class_="summary-answer-num").get_text()
                        result_list["result_list"].append(item_ins)
                    except BaseException as e:
                        logging.error("Parse 360 result error. ErrorMsg: %s" % str(e))
        except BaseException as e:
            logging.error("Get ZhiHu search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    url_list = ZhiHuSearch.search_page("区块链", page=3)    # 已经测试过了,运行正常
    for item in url_list["result_list"]:
        print(item)
