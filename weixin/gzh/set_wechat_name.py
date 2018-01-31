# coding=utf-8

import requests
from bs4 import BeautifulSoup
import time

from customize_website.Util import Util
from customize_website.database import DBUtil


class WeChatMap(object):
    """
    设置微信公众号名称与biz对应的map，结果保存在数据库中。
    从公众号爬取文章中选择biz以及链接，去网页上爬取公众号名称。
    """
    create_wechat_biz_map_sql = "CREATE TABLE IF NOT EXISTS article_wechat_map(" \
                                "id INT PRIMARY KEY  AUTO_INCREMENT," \
                                "biz VARCHAR(100)," \
                                "wechat VARCHAR(100)" \
                                ");"
    select_biz_sql_format = "SELECT * FROM article_wechat_map WHERE wechat = \"{}\""  # 根据公众号的名称查询

    insert_biz_sql_format = "INSERT INTO article_wechat_map(biz, wechat) VALUES(\"{}\", \"{}\")"

    @staticmethod
    def create_table():
        DBUtil.select_data(WeChatMap.create_wechat_biz_map_sql)

    @staticmethod
    def get_biz():
        sql = "select distinct biz from article_wechat"
        result_list = []
        result_dict = DBUtil.select_datas(sql)
        if result_dict:
            for item_dict in result_dict:
                result_list.append(item_dict['biz'])
        return result_list

    @staticmethod
    def get_link(biz):
        sql = "select link from article_wechat where biz=\"{}\" limit 1".format(biz)
        result = DBUtil.select_data(sql)
        link = ""
        if result:
            link = result["link"]
        return link

    @staticmethod
    def get_wechat_name(link):
        """
        通过公众号文章抓取公众号名称。
        :param link:  公众号某一篇文章的地址
        :return: 公众号名称
        """
        r = requests.get(link)
        bs_obj = BeautifulSoup(r.content, "html.parser")
        link_tag = bs_obj.find("a", id="post-user")
        name = ""
        if link_tag:
            name = Util.all_strip(link_tag.get_text())
        return name

    @staticmethod
    def save_name_biz_map(biz, name):
        select_sql_new = WeChatMap.select_biz_sql_format.format(biz)
        result = DBUtil.select_data(select_sql_new)
        if not result:
            insert_sql_new = WeChatMap.insert_biz_sql_format.format(biz, name)
            DBUtil.insert_data(insert_sql_new)

    @staticmethod
    def set_wechat_name_map():
        WeChatMap.create_table()
        biz_list = WeChatMap.get_biz()
        for biz in biz_list:
            if biz == ' "MjM5MzkyMzMzNA=="':
                continue
            link = WeChatMap.get_link(biz)
            if link:
                name = WeChatMap.get_wechat_name(link)
                if name:
                    WeChatMap.save_name_biz_map(biz, name)
                    time.sleep(1)


if __name__ == "__main__":
    WeChatMap.set_wechat_name_map()
