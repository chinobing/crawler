# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import requests


class TouZhongWangSearch(object):
    """
    利用雷锋网搜索得到的文章的结果.
    """

    search_url = "https://www.leiphone.com/search?s={}"

    page_url = "https://www.leiphone.com/search?s={}&site=article&page={}"

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
            url = LeiFengSearch.search_url.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result_links = bs_obj.find("ul", class_="articleList").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(LeiFengSearch.item)
                            title_node = result.find("div", class_="txt")
                            item_ins['link'] = title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("div", class_="des").get_text()
                            item_ins["date"] = result.find("div", class_="time").get_text()
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
    def search_page(key_word, page):
        """
        Get specified page of the site. 
        :param key_word: 
        :param page: 
        :return: 
        """
        result_list = {"result_list": []}
        try:
            key_word_quote = parse.quote(key_word)
            url = LeiFengSearch.page_url.format(key_word_quote, page)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result_links = bs_obj.find("ul", class_="articleList").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(LeiFengSearch.item)
                            title_node = result.find("div", class_="txt")
                            item_ins['link'] = title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("div", class_="des").get_text()
                            item_ins["date"] = result.find("div", class_="time").get_text()
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
            logging.error("Get LeiFeng search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    url_list = LeiFengSearch.search_page("区块链", page=4)    # 已经测试过了,运行正常
    for item in url_list["result_list"]:
        print(item)
