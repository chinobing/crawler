# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import requests


class YiGuanZhiKuSearch(object):
    """
    利用搜狗搜索得到的微信文章的结果.
    """

    ori_url = "http://www.199it.com/archives/tag/%E6%98%93%E8%A7%82%E6%99%BA%E5%BA%93"

    search_page_url = "http://s.199it.com/cse/"

    item = {"title": None, "abstract": None, "link": None, "date": ""}

    @staticmethod
    def get_search_url():
        """
        从易观智库的网站中提取出url中需要的参数,因为易观智库没有这些参数无法直接调用url得到搜索的结果.
        :return: 带有参数的可以搜索的url,返回后需要填充
        """
        url = "http://s.199it.com/cse/search"
        try:
            r = requests.get(YiGuanZhiKuSearch.ori_url)
            bs_obj = BeautifulSoup(r.content, "html.parser")
            txt = bs_obj.get_text()
            start_pos = txt.find("js?sid=")
            end_pos = txt.find("'", start_pos)
            para_s = txt[start_pos + 7: end_pos]
            para_entry = "1"
            url += "?s=" + para_s + "&entry=" + para_entry + "&q={}"
        except BaseException as e:
            logging.error("Get search url parameter error.")
            raise BaseException("Get search url parameter error.")
        return url

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
            url = YiGuanZhiKuSearch.get_search_url().format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result_links = bs_obj.find("div", id="results").findAll("div", class_="result f s0")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(YiGuanZhiKuSearch.item)
                            title_node = result.find("h3", class_="c-title").find("a")
                            item_ins['link'] = title_node.get("href")
                            item_ins['title'] = title_node.get_text()
                            # 乐晴智库没有摘要,目前用标签代替.
                            item_ins['abstract'] = result.find("div", class_="c-abstract").get_text()
                            item_ins["date"] = result.find("span", class_="c-showurl").get_text().split(" ")[1]
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse YiGuanZhiKu result error. ErrorMsg: %s" % str(e))
                    next_page = bs_obj.find("a", class_="pager-next-foot n")
                    if next_page:
                        url = YiGuanZhiKuSearch.search_page_url + next_page.get("href")
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
            logging.error("Get YiGuanZhiKu search result error. ErrorMsg: %s" % str(e))
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
            url = YiGuanZhiKuSearch.get_search_url().format(key_word_quote) + "&p=" + str(page)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result_links = bs_obj.find("div", id="results").findAll("div", class_="result f s0")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(YiGuanZhiKuSearch.item)
                            title_node = result.find("h3", class_="c-title").find("a")
                            item_ins['link'] = title_node.get("href")
                            item_ins['title'] = title_node.get_text()
                            # 乐晴智库没有摘要,目前用标签代替.
                            item_ins['abstract'] = result.find("div", class_="c-abstract").get_text()
                            item_ins["date"] = result.find("span", class_="c-showurl").get_text().split(" ")[1]
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse YiGuanZhiKu result error. ErrorMsg: %s" % str(e))
                    break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get YiGuanZhiKu search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    url_list = YiGuanZhiKuSearch.search_page("资本", 3)    # 已经测试过了,运行正常
    for res in url_list["result_list"]:
        print(res)
