# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import requests


class TouZiJieSearch(object):
    """
    利用雷锋网搜索得到的文章的结果.
    """

    site_url = "http://search.pedaily.cn"

    news_search_url = "http://search.pedaily.cn/k{}-t2"

    new_page_url = "http://search.pedaily.cn/k{}-t2-p{}"

    company_search_url = "http://search.pedaily.cn/k{}-t3"

    company_page_url = "http://search.pedaily.cn/k{}-t3-p{}"

    report_search_url = "http://search.pedaily.cn/k{}-t10"

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
            key_word_quote = parse.quote(key_word)
            url = TouZiJieSearch.news_search_url.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result_links = bs_obj.find("ul", class_="news-list").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(TouZiJieSearch.item)
                            title_node = result.find("h3")
                            item_ins['link'] = title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("div", class_="intr").get_text()
                            item_ins["date"] = result.find("span", class_="date").get_text()
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse LeiFeng result error. ErrorMsg: %s" % str(e))
                    next_page = bs_obj.find("a", class_="next")
                    if next_page:
                        url = TouZiJieSearch.site_url + next_page.get("href")
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
            logging.error("Get TouZiJie search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def news_page_search(key_word, page):
        """
        Get specified page of the site. 
        :param key_word: 
        :param page: 
        :return: 
        """
        result_list = {"result_list": []}
        try:
            key_word_quote = parse.quote(key_word)
            url = TouZiJieSearch.new_page_url.format(key_word_quote, page)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result_links = bs_obj.find("ul", class_="news-list").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(TouZiJieSearch.item)
                            title_node = result.find("h3")
                            item_ins['link'] = title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("div", class_="intr").get_text()
                            item_ins["date"] = result.find("span", class_="date").get_text()
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
            logging.error("Get TouZiJie search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def company_search(key_word, search_page=5):
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
            url = TouZiJieSearch.company_search_url.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result_links = bs_obj.find("ul", class_="news-list").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(TouZiJieSearch.item)
                            title_node = result.find("h3")
                            item_ins['link'] = title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("div", class_="txt").find("div").get_text()
                            # item_ins["date"] = result.find("span", class_="date").get_text()  # 投资界的企业是没有时间的.
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse LeiFeng result error. ErrorMsg: %s" % str(e))
                    next_page = bs_obj.find("a", class_="next")
                    if next_page:
                        url = TouZiJieSearch.site_url + next_page.get("href")
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
            logging.error("Get TouZiJie search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def company_page_search(key_word, page):
        """
        Get specified page of the site. 
        :param key_word: 
        :param page: 
        :return: 
        """
        result_list = {"result_list": []}
        try:
            key_word_quote = parse.quote(key_word)
            url = TouZiJieSearch.company_page_url.format(key_word_quote, page)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result_links = bs_obj.find("ul", class_="news-list").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(TouZiJieSearch.item)
                            title_node = result.find("h3")
                            item_ins['link'] = title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("div", class_="txt").find("div").get_text()
                            # item_ins["date"] = result.find("span", class_="date").get_text()  # 投资界的企业是没有时间的.
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
            logging.error("Get TouZiJie search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def search(key_word, search_page=5):
        """
        利用关键字进行搜索, 搜索结果返回指定页数,
        :param key_word: 关键字.
        :param search_page: 需要返回几页结果.
        :return: 返回字典, {} 
        """
        news_lists = TouZiJieSearch.news_search(key_word, search_page)
        company_lists = TouZiJieSearch.company_search(key_word, search_page)
        news_lists['result_list'] = news_lists['result_list'] + company_lists['result_list']
        return news_lists

    @staticmethod
    def search_page(key_word, page):
        """
        Get specified page of the site. 
        :param key_word: 
        :param page: 
        :return: 
        """
        news_lists = TouZiJieSearch.news_page_search(key_word, page)
        company_lists = TouZiJieSearch.company_page_search(key_word, page)
        news_lists["result_list"] = news_lists['result_list'] + company_lists['result_list']
        return news_lists

if __name__ == "__main__":
    url_list = TouZiJieSearch.search_page("区块链", page=3)    # 已经测试过了,运行正常
    for item in url_list["result_list"]:
        print(item)
