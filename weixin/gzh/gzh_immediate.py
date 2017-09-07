# coding=utf-8

from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import re
import json
from customize_website.database import DBUtil
import html as htmlparser


class WeChatSubscriptionRealTimeCrawler():
    """
    时实爬微信公众号的内容,利用搜狗搜索到指定的公众号的名称,然后进入爬前十条.
    """
    sougou_search_url = "http://weixin.sogou.com/weixin?type=1" \
                        "&s_from=input&query={}&ie=utf8"
    select_sql = ""
    insert_sql = ""
    select_biz = "SELECT * FROM article_wechat_map WHERE wechat = \"{}\""

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
        json_str = pattern.findall(content)[0]
        biz = self.get_biz(self.name)
        self.parse_json(json_str, biz)

    def parse_json(self, json_str, biz):
        try:
            msg_list = json.loads(json_str)['list']
        except Exception as e:
            msg_list = json.loads(htmlparser.unescape(json_str))['list']
        for msg in msg_list:
            app_msg_ext_info = msg['app_msg_ext_info']
            self.get_info(app_msg_ext_info, biz)
            is_multi = app_msg_ext_info['is_multi']
            if is_multi:
                multi_app_msg_item_list = app_msg_ext_info['multi_app_msg_item_list']
                for multi_msg in multi_app_msg_item_list:
                    self.get_info(multi_msg, biz)

    @staticmethod
    def get_info(msg_dict, biz):
        title = htmlparser.escape(msg_dict['title'])
        content_url = htmlparser.unescape(msg_dict['content_url']).replace("\\", "")
        # source_url = htmlparser.unescape(msg_dict['source_url']).replace("\\", "")
        result = DBUtil.select_data(WeChatSubscriptionRealTimeCrawler.select_sql.format(content_url))
        # 如果该文章不在数据库中
        if not result:
            DBUtil.insert_data(WeChatSubscriptionRealTimeCrawler.insert_sql.format(biz, title, content_url))

    def get_biz(self, wechat):
        result = DBUtil.select_data(self.select_biz.format(wechat))
        if result:
            return result['biz']
        else:
            return ""
