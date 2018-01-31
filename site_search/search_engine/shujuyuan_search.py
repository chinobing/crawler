# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
import time


class ShuJuYuanSearch(object):
    """
    ShuJuYuan crawler. Get the search content in www.datayuan.cn
    """
    # 网页搜索入口
    search_url = "http://www.datayuan.cn/search?q={}"

    item = {"title": None, "abstract": None, "link": None, "date": ""}

    @staticmethod
    def search(key_word, search_page=5):
        """
        利用关键字进行搜索, 搜索结果返回指定页数.数据猿这个网站的搜索一次会加载很多,然后通过点击加载更多动态加载页面,
        基本无法直接找到哪一页. 只能自己更具得到的结构进行分隔.
        :param key_word: 关键字.
        :param search_page: 需要返回几页结果.
        :return: 返回字典, {} 
        """
        result_list = {"result_list": []}
        max_page = search_page
        try:
            key_word_quote = parse.quote(key_word)
            url = ShuJuYuanSearch.search_url.format(key_word_quote)
            driver = webdriver.PhantomJS(
                executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
            driver.set_page_load_timeout(30)
            driver.get(url)
            time.sleep(0.5)
            driver.implicitly_wait(10)
            logging.info("Get %s success." % url)
            page_cnt = driver.page_source
            while 1:
                max_page -= 1
                if max_page <= 0:
                    if page_cnt:
                        bs_obj = BeautifulSoup(page_cnt, "html.parser")
                        result_links = bs_obj.find("div", class_="main-div-l").findAll("div", class_="wz-div")
                        for result in result_links:
                            try:
                                item_ins = deepcopy(ShuJuYuanSearch.item)
                                title_node = result.find("h2").find("a")
                                item_ins['link'] = title_node.get("href")
                                item_ins['title'] = title_node.get_text()
                                item_ins['abstract'] = result.find("div", class_="wz-div-text").get_text()
                                item_ins['date'] = result.find("div", class_="nametime").get_text()
                                result_list["result_list"].append(item_ins)
                            except BaseException as e:
                                logging.error("Parse 36kr result error. ErrorMsg: %s" % str(e))
                    break
                driver.find_element_by_class_name("morediv").find_element_by_tag_name("a").click()
                driver.refresh()
                time.sleep(0.5)
                page_cnt = driver.page_source
        except BaseException as e:
            logging.error("Get ShuJuYuan search result error. ErrorMsg: %s" % str(e))
        finally:
            driver.quit()
        return result_list


if __name__ == "__main__":
    url_list = ShuJuYuanSearch.search('区块链', 1)["result_list"]
    for item in url_list:
        print(item)
