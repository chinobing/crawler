# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import requests
import re


class HuXiuSearch(object):
    """
    利用搜狗搜索得到的微信文章的结果.
    """

    search_url = "https://www.huxiu.com/search.html?s={}"
    search_page_url="https://www.huxiu.com/search.html?s={}&sort=&per_page={}"

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
        cur_page = 1  # 用于循环爬取下一页
        max_page = search_page
        try:
            key_word_quote = parse.quote(key_word)
            url = HuXiuSearch.search_url.format(key_word_quote)
            url_for_next=url
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                # 虎嗅网有简单的防爬虫机制
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20'})
                # print(r.text)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    # 如果一个页面的class属性为rb, 则此链接点击进去后不是一个单独的与页面,此处记录一下即可.
                    result_links = bs_obj.find("ul", class_="search-wrap-list-ul").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(HuXiuSearch.item)
                            title_node = result.find("h2")
                            item_ins['link'] = "https://www.huxiu.com" + title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("div", class_="mob-summay").get_text()
                            item_ins["date"] = result.find("span", class_="time").get_text()
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse Huxiu result error. ErrorMsg: %s" % str(e))
                    # next_page = bs_obj.find("ul", class_="pagination")
                    cur_page += 1
                    next_page = url_for_next+"&sort=&per_page="+str(cur_page)
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
            logging.error("Get Huxiu search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def search_page(key_word, page):
        """
        爬取特定的页面
        :param key_word:
        :param page:
        :return:
        """
        result_list = {"result_list": []}
        try:
            key_word_quote = parse.quote(key_word)
            url = HuXiuSearch.search_page_url.format(key_word_quote, page)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20'})
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    # 如果一个页面的class属性为rb, 则此链接点击进去后不是一个单独的与页面,此处记录一下即可.
                    result_links = bs_obj.find("ul", class_="search-wrap-list-ul").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(HuXiuSearch.item)
                            title_node = result.find("h2")
                            item_ins['link'] = "https://www.huxiu.com" + title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("div", class_="mob-summay").get_text()
                            item_ins["date"] = result.find("span", class_="time").get_text()
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse Huxiu result error. ErrorMsg: %s" % str(e))
                    break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get Huxiu search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    url_list = HuXiuSearch.search_page("区块链", page=3)  # 已经测试过了,运行正常
    # print(url_list["result_list"])
    for t in url_list["result_list"]:
        print(t)
