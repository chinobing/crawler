# coding=utf-8

from urllib import parse
import requests
from bs4 import BeautifulSoup


class GetLinkFromTitle(object):
    """
        实时爬取公众号的文章得到的链接地址不是永久有效的,因此需要对地址做一下转化,
        在用户需要跳转到源网页的时候可以给出当前有效的地址.
        得到最新的文章地址主要还是利用搜狗搜索,利用公众号名称以及文章题目搜索文章,
        基本第一条就是所需要的东西.
    """
    search_url = "http://weixin.sogou.com/weixin?type=2&s_from=input&query={}+{}&ie=utf8&_sug_=n&_sug_type_="

    @staticmethod
    def get_link(title, wechat_name):
        try:
            title = parse.quote(title)
            wechat_name = parse.quote(wechat_name)
            url = GetLinkFromTitle.search_url.format(title, wechat_name)
            r = requests.get(url)
            bs_obj = BeautifulSoup(r.content, "html.parser")
            h_tag = bs_obj.find("h3")
            link = h_tag.find("a").get("href")
            return link
        except BaseException as e:
            print("ErrorMsg: %s" % str(e))
            return ""  # 如果错误可以返回错误页面的处理地址. 但是目前没有错误页面的返回地址


if __name__ == "__main__":
    print(GetLinkFromTitle.get_link("当马云、马化腾、贾跃亭等大佬化身王者荣耀的英雄...", '36氪'))