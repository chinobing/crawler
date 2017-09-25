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
    公众号的名称与biz的映射已经保存在表中,直接遍历表即可.
    """
    sougou_search_url = "http://weixin.sogou.com/weixin?type=1" \
                        "&s_from=input&query={}&ie=utf8"
    prefix_url = 'https://mp.weixin.qq.com'
    select_sql = "select * from article_wechat where link = '{}'"
    insert_sql = "insert into article_wechat(biz, link, title) VALUES('{}', '{}', '{}')"
    select_map = "SELECT biz, wechat FROM article_wechat_map"

    @staticmethod
    def get_biz_wechat_map():
        result = DBUtil.select_datas(WeChatSubscriptionRealTimeCrawler.select_map)
        if not result:
            result = []
        return result

    @staticmethod
    def traverse_all_wechat():
        wechat_map = WeChatSubscriptionRealTimeCrawler.get_biz_wechat_map()
        for item in wechat_map:
            wechat = item.get("wechat")
            biz = item.get("biz")
            WeChatSubscriptionRealTimeCrawler.crawl_first_ten(biz=biz, wechat_name=wechat)

    @staticmethod
    def get_wechat_subscription_link(name):
        key = quote(name)
        url_new = WeChatSubscriptionRealTimeCrawler.sougou_search_url.format(key)
        r = requests.get(url_new)
        bs_obj = BeautifulSoup(r.content, "lxml")
        link = bs_obj.find("a", uigs="account_name_0")
        if link:
            return link.get("href")
        else:
            return ""

    @staticmethod
    def crawl_first_ten(biz, wechat_name):
        wechat_subscription_link = WeChatSubscriptionRealTimeCrawler.get_wechat_subscription_link(wechat_name)
        r = requests.get(wechat_subscription_link)
        try:
            content = r.content.decode("utf-8")
        except:
            content = r.content.decode("gbk")
        pattern = re.compile(r'msgList = (.*?});')
        json_str = pattern.findall(content)[0]
        WeChatSubscriptionRealTimeCrawler.parse_json(json_str, biz)

    @staticmethod
    def parse_json(json_str, biz):
        try:
            msg_list = json.loads(json_str)['list']
        except Exception as e:
            msg_list = json.loads(htmlparser.unescape(json_str))['list']
        for msg in msg_list:
            app_msg_ext_info = msg['app_msg_ext_info']
            WeChatSubscriptionRealTimeCrawler.get_info(app_msg_ext_info, biz)
            is_multi = app_msg_ext_info['is_multi']
            if is_multi:
                multi_app_msg_item_list = app_msg_ext_info['multi_app_msg_item_list']
                for multi_msg in multi_app_msg_item_list:
                    WeChatSubscriptionRealTimeCrawler.get_info(multi_msg, biz)

    @staticmethod
    def get_info(msg_dict, biz):
        title = htmlparser.escape(msg_dict['title'])
        content_url = WeChatSubscriptionRealTimeCrawler.prefix_url + htmlparser.unescape(msg_dict['content_url']).replace("\\", "")
        result = DBUtil.select_data(WeChatSubscriptionRealTimeCrawler.select_sql.format(content_url))
        # 如果该文章不在数据库中, 则插入数据,问题的关键是link从搜狗爬的与从西瓜爬的不一样.
        if not result:
            DBUtil.insert_data(WeChatSubscriptionRealTimeCrawler.insert_sql.format(biz, content_url, title))


if __name__ == "__main__":
    WeChatSubscriptionRealTimeCrawler.traverse_all_wechat()
