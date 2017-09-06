# coding=utf-8

from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import re


class WeChatSubscriptionRealTimeCrawler():
    """
    时实爬微信公众号的内容,利用搜狗搜索到指定的公众号的名称,然后进入爬前十条.
    """
    sougou_search_url = "http://weixin.sogou.com/weixin?type=1" \
                        "&s_from=input&query={}&ie=utf8"

    def __init__(self, name):
        self.name = name

    def get_wechat_subscription_link(self):
        key = quote(self.name)
        url_new = self.sougou_search_url.format(key)
        r = requests.get(url_new)
        bs_obj = BeautifulSoup(r.content, "lxml")
        link = bs_obj.find("a", uigs="account_name_0")
        if link:
            return link.get("href")
        else:
            return ""

    def crawl_first_ten(self):
        wechat_subscription_link = self.get_wechat_subscription_link()
        r = requests.get(wechat_subscription_link)
        try:
            content = r.content.decode("utf-8")
        except:
            content = r.content.decode("gbk")
        pattern = re.compile(r'msgList = (.*?);')
        pattern.findall(content)
