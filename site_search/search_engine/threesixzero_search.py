# coding=utf-8

import requests
from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import html
import re


class ThreeSixZero(object):
    """
    360搜索引擎搜索的结果,
    """

    page_url_format = "https://www.so.com/s?ie=utf-8&fr=none&src=360sou_newhome&q={}"   # 匹配parse过的关键词即可.

    # 360搜索引擎最新消息(新闻页面的搜索)的url
    news_url_format = "http://news.so.com/ns?q={}"

    three_six_zero_url = "https://www.so.com"

    item = {"title": None, "abstract": None, "link": None}

    @staticmethod
    def search(key_word, search_page=5):
        """sougou
        根据关键字进行搜索,使用360搜索引擎,默认使用五页的搜索结果.
        目前还有一些链接的格式abstract没有固定,导致解析出错.
        :param key_word: 关键字
        :param search_page: 需要使用的搜索页数.
        :return: 搜索得到的结果,以字典的形式返回.
        """
        result_list = {"result_list": []}
        max_page = search_page
        try:
            key_word_quote = parse.quote(key_word)
            url = ThreeSixZero.page_url_format.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    # result = bs_obj.findAll("li", attrs={"class": re.compile(r'result\s.*')})
                    result_links = bs_obj.findAll("li", class_="res-list")
                    for result in result_links:
                        try:
                            link = result.findAll("h3", class_="res-title")
                            if len(link) == 1:
                                link = link[0]
                                title = link.get_text()
                                href = link.find("a").get("href")
                                abstract = link.parent.find("div", class_="res-comm-con")
                                if not abstract:
                                    abstract = link.parent.find("p", class_="res-desc")
                                abstract = abstract.get_text()
                                if title and url and abstract:
                                    item_ins = deepcopy(ThreeSixZero.item)
                                    item_ins['link'] = href
                                    item_ins['title'] = title
                                    item_ins['abstract'] = abstract
                                    result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse 360 result error. ErrorMsg: %s" % str(e))
                    next_page = bs_obj.find("a", id="snext")
                    if next_page:
                        url = ThreeSixZero.three_six_zero_url + next_page.get("href")
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
    def news_search(key_word):
        pass


if __name__ == "__main__":
    result_list1 = ThreeSixZero.search("区块链")
    print(result_list1["result_list"])
