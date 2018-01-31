# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import requests
import re


class YiOuSearch(object):
    """
    利用搜狗搜索得到的微信文章的结果.
    """

    search_url = "https://www.iyiou.com/search/{}"
    search_page_url = "https://www.iyiou.com/search?p={}&page={}.html"

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
        cur_page = 1  # 用于循环爬取下一页
        try:
            key_word_quote = parse.quote(key_word)
            url = YiOuSearch.search_url.format(key_word_quote)
            url_for_next = url
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                # print(r.text)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    # 如果一个页面的class属性为rb, 则此链接点击进去后不是一个单独的与页面,此处记录一下即可.
                    result_links = bs_obj.find("ul", class_="newestArticleList").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(YiOuSearch.item)
                            title_node = result.find("div", class_="text fl")
                            item_ins['link'] = "https://www.iyiou.com" + title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins["date"] = title_node.find("div", class_="time").get_text()
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse YiOu result error. ErrorMsg: %s" % str(e))
                    # next_page = bs_obj.find("ul", class_="pagination")
                    cur_page += 1
                    next_page = url_for_next + "/page" + str(cur_page)+".html"
                    url = next_page
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
            logging.error("Get YiOu search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def search_page(key_word, page):
        """
        利用关键字进行搜索, 搜索结果返回指定页数,
        :param key_word: 关键字.
        :param page: 需要返回几页结果.
        :return: 返回字典, {}
        """
        result_list = {"result_list": []}
        try:
            key_word_quote = parse.quote(key_word)
            url = YiOuSearch.search_page_url.format(key_word_quote,page)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20'})
                #print(r.text)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content,"html.parser")
                    # 如果一个页面的class属性为rb, 则此链接点击进去后不是一个单独的与页面,此处记录一下即可.
                    result_links = bs_obj.find("ul", class_="newestArticleList").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(YiOuSearch.item)
                            title_node = result.find("div", class_="text fl")
                            item_ins['link'] = "https://www.iyiou.com"+title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins["date"] = title_node.find("div", class_="time").get_text()
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse YiOu result error. ErrorMsg: %s" % str(e))
                    break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get YiOu search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    #url_list = YiOuSearch.search("人工智能", search_page=3)    # 已经测试过了,运行正常
    #print(url_list["result_list"])
    #for t in url_list["result_list"]:
        #print(t)

    url_list = YiOuSearch.search_page("人工智能", page=3)  # 已经测试过了,运行正常
    # print(url_list["result_list"])
    for t in url_list["result_list"]:
        print(t)
