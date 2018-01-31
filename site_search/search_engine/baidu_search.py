# coding=utf-8

import requests
import re
from urllib.parse import quote
import html
from bs4 import BeautifulSoup
import logging
from copy import deepcopy


class BaiDuSearch(object):
    """
    百度的搜索结果,目前只抓取,不保存.
    """
    # 网页搜索入口,
    page_url_format = "http://www.BaiDu.com/s?ie=UTF-8&wd={}"

    # 注意这是新闻的搜索入口, 不要改动参数的值,否则搜到的结果会不一样
    news_url_format = "http://www.BaiDu.com/s?wd={}&pn=0&tn=BaiDurt&ie=utf-8&rtt=1&bsst=1"

    BaiDu_url = "http://www.BaiDu.com"          # 注意后面没有 "/"

    item = {"title": None, "abstract": None, "link": None, "date": ""}

    @staticmethod
    def parse_BaiDu_link(url):
        """
        从百度的链接中得到目标网页的链接.
        :param url: 百度的url
        :return: 
        """
        try:
            r = requests.get(url, allow_redirects=False)
            location = r.headers["Location"]
            return location
        except Exception as e:
            logging.error("Get original link from BaiDu error. ErrorMsg: %s" % str(e))
            raise BaseException()   # 抛出异常

    @staticmethod
    def search(key_word, max_page):
        """
        百度搜索的结果,
        返回的结果已经通过了html.escape处理,转义了所有特殊字符.
        :param key_word: 关键字
        :param max_page: 最多取几页结果.
        :return: {'result_list': [{'title': 'xxx', 'abstract': 'xxx', 'link': 'http://xxx.xxx'}, {...}, ...]}
        """
        result_list = {'result_list': []}
        try:
            key_word_quote = quote(key_word)
            url = BaiDuSearch.page_url_format.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    # result-op c-container xpath-log 这个是百度百科的class, 另外百度的自己的东西貌似都是用的这个特殊的class.
                    result = bs_obj.findAll("div", attrs={"class": re.compile(r'result c-container')})
                    for href in result:
                        try:
                            item_ins = deepcopy(BaiDuSearch.item)
                            link_tag = href.find("h3").find('a')
                            item_ins["link"] = BaiDuSearch.parse_BaiDu_link(link_tag.get("href"))
                            item_ins["title"] = BaiDuSearch.escape_and_strip(link_tag.get_text())
                            # 摘要部分在百度百科上面出了问题,那个部分的摘要的格式并不是确定的.
                            item_ins["abstract"] = BaiDuSearch.escape_and_strip(href.find("div", class_="c-abstract").get_text())
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse BaiDu result error. ErrorMsg: %s" % str(e))
                    next_page = bs_obj.find("a", class_="n")
                    # Get Baidu Baike information
                    baike = bs_obj.find("div", class_="result-op c-container xpath-log")
                    if baike:
                        try:
                            item_ins = deepcopy(BaiDuSearch.item)
                            link_tag = baike.find("h3").find("a")
                            item_ins["link"] = BaiDuSearch.parse_BaiDu_link(link_tag.get("href"))
                            item_ins["title"] = BaiDuSearch.escape_and_strip(link_tag.get_text())
                            item_ins["abstract"] = baike.find("div", class_="c-row").get_text()
                            result_list["result_list"].insert(0, item_ins)
                        except BaseException as e:
                            logging.error("Get BaiKe error in BaiDu. Error Msg: %s" % str(e))
                    if next_page:
                        url = BaiDuSearch.BaiDu_url + next_page.get("href")
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
            logging.error("Get BaiDu search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def get_news_from_BaiDu(key_word, max_page):
        """
        百度搜索新闻的结果
        返回的结果已经通过了html.escape处理,转义了所有特殊字符.
        :param key_word: 关键字
        :param max_page: 最多取几页结果.
        :return: {'result_list': [{'title': 'xxx', 'abstract': 'xxx', 'link': 'http://xxx.xxx'}, {...}, ...]}
        """
        result_list = {'result_list': []}
        key_word_quote = quote(key_word)
        url = BaiDuSearch.news_url_format.format(key_word_quote)
        failure = 0
        try:
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result = bs_obj.findAll("table", attrs={"class": "result"})
                    for href in result:
                        try:
                            item_ins = deepcopy(BaiDuSearch.item)
                            link_tag = href.find('h3').find('a')
                            item_ins["link"] = link_tag.get("href")
                            item_ins["title"] = BaiDuSearch.escape_and_strip(link_tag.get_text())
                            item_ins["abstract"] = BaiDuSearch.escape_and_strip(href.find("font").get_text())
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse BaiDu result error. ErrorMsg: %s" % str(e))
                    next_page = bs_obj.find("a", class_="n")
                    if next_page:
                        url = BaiDuSearch.BaiDu_url + '/' + next_page.get("href")  # 注意此处需要 "/", 百度网页上得到的链接没有 "/"
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
            logging.error("Get news from BaiDu error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def escape_and_strip(line):
        # \xa0 是unicode中的中文空格, 过滤掉空字符.
        line = line.replace("\r", "").replace("\n", "").replace("\t", "").replace("\xa0", '').replace(" ", '')
        return html.escape(line)

    @staticmethod
    def search_page(key_word, page):
        """
        get target page 
        :param key_word: 
        :param page: 
        :return: 
        """
        result_list = {'result_list': []}
        try:
            key_word_quote = quote(key_word)
            # 需要先从初始页面进去,在进入到制定页面,因为有参数控制,不能直接进入制定页面.
            url = BaiDuSearch.page_url_format.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    next_page = bs_obj.find("a", class_="n")
                    if next_page:
                        url = BaiDuSearch.BaiDu_url + next_page.get("href")
                        start = url.find("&pn=")
                        end = url.find("&", start + 4)
                        url = url[:start + 4] + str(page * 10) + url[end:]
                        r = requests.get(url)
                        bs_obj = BeautifulSoup(r.content, "html.parser")
                        # result-op c-container xpath-log 这个是百度百科的class, 另外百度的自己的东西貌似都是用的这个特殊的class.
                        result = bs_obj.findAll("div", attrs={"class": re.compile(r'result c-container')})
                        for href in result:
                            try:
                                item_ins = deepcopy(BaiDuSearch.item)
                                link_tag = href.find("h3").find('a')
                                item_ins["link"] = BaiDuSearch.parse_BaiDu_link(link_tag.get("href"))
                                item_ins["title"] = BaiDuSearch.escape_and_strip(link_tag.get_text())
                                # 摘要部分在百度百科上面出了问题,那个部分的摘要的格式并不是确定的.
                                item_ins["abstract"] = BaiDuSearch.escape_and_strip(
                                    href.find("div", class_="c-abstract").get_text())
                                result_list["result_list"].append(item_ins)
                            except BaseException as e:
                                logging.error("Parse BaiDu result error. ErrorMsg: %s" % str(e))
                        url = ""
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get BaiDu search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    url_list = BaiDuSearch.search_page('区块链', 5)["result_list"]
    for item in url_list:
        print(item)
