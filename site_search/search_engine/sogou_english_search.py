# coding=utf-8

import requests
from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import re


class SoGouEnglishSearch(object):
    """
    搜狗搜索的结果
    """

    page_url_format = "http://english.sogou.com/english?query={}"  # 匹配parse过的关键词即可.

    sogou_url = "http://english.sogou.com/english"   # 此处需要加上web,因为下一页给出的地址只有参数

    item = {"title": None, "abstract": None, "link": None, "date": ""}

    @staticmethod
    def search(key_word, search_page=5):
        """
        利用关键字进行搜索, 搜索结果返回指定页数,
        搜狗搜索的网页结果并不是很规范,并不是单独网页,有的有多个页面.
        因此如果只取单独网页,结果较少,包含多个链接的结果也过于繁琐.
        :param key_word: 关键字.
        :param search_page: 需要返回几页结果.
        :return: 返回字典, {} 
        """
        result_list = {"result_list": []}
        max_page = search_page
        try:
            key_word_quote = parse.quote(key_word)
            url = SoGouEnglishSearch.page_url_format.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    # 如果一个页面的class属性为rb, 则此链接点击进去后不是一个单独的与页面,此处记录一下即可.
                    result_links = bs_obj.findAll("div", attrs={"class": re.compile(r'vrwrap|rb')})
                    for result in result_links:
                        try:
                            link = result.find("h3", attrs={"class": re.compile(r'vrTitle|pt')})
                            contains = result.find("div", class_="str-pd-box")
                            if not contains and link:
                                title = link.get_text()
                                href = link.find("a").get("href")
                                if len(href) == 0:
                                    continue
                                # abstract这里可能还有一些错误,可能还有其他格式.
                                abstract = result.find("p")
                                if not abstract:
                                    abstract = link.parent.find("div", class_="ft")
                                abstract = abstract.get_text()
                                if title and url and abstract:
                                    item_ins = deepcopy(SoGouEnglishSearch.item)
                                    item_ins['link'] = href
                                    item_ins['title'] = title
                                    item_ins['abstract'] = abstract
                                    result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse SoGou result error. ErrorMsg: %s" % str(e))
                    next_page = bs_obj.find("a", id="sogou_next")
                    if next_page:
                        url = SoGouEnglishSearch.sogou_url + next_page.get("href")
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
            logging.error("Get SoGou search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def news_search(keyword, search_page=5):
        pass

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
            url = SoGouEnglishSearch.page_url_format.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    # 如果一个页面的class属性为rb, 则此链接点击进去后不是一个单独的与页面,此处记录一下即可.

                    next_page = bs_obj.find("a", id="sogou_next")
                    if next_page:
                        url = SoGouEnglishSearch.sogou_url + next_page.get("href")
                        start = url.find("&page=")
                        end = url.find("&", start + 6)
                        url = url[:start + 6] + str(page) + url[end:]
                        r = requests.get(url)
                        bs_obj = BeautifulSoup(r.content, "html.parser")
                        result_links = bs_obj.findAll("div", attrs={"class": re.compile(r'vrwrap|rb')})
                        for result in result_links:
                            try:
                                link = result.find("h3", attrs={"class": re.compile(r'vrTitle|pt')})
                                contains = result.find("div", class_="str-pd-box")
                                if not contains and link:
                                    title = link.get_text()
                                    href = link.find("a").get("href")
                                    if len(href) == 0:
                                        continue
                                    # abstract这里可能还有一些错误,可能还有其他格式.
                                    abstract = result.find("p")
                                    if not abstract:
                                        abstract = link.parent.find("div", class_="ft")
                                    abstract = abstract.get_text()
                                    if title and url and abstract:
                                        item_ins = deepcopy(SoGouEnglishSearch.item)
                                        item_ins['link'] = href
                                        item_ins['title'] = title
                                        item_ins['abstract'] = abstract
                                        result_list["result_list"].append(item_ins)
                            except BaseException as e:
                                logging.error("Parse SoGou result error. ErrorMsg: %s" % str(e))
                        break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get SoGou search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    url_list = SoGouEnglishSearch.search_page("capital", 2)    # 已经测试过了,
    for item in url_list["result_list"]:
        print(item)
