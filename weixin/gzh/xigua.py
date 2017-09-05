import requests
from bs4 import BeautifulSoup
import re
from customize_website.database import DBUtil
import logging
import html
import time
import datetime

# 将cookie字符串转换为字典
cookies_dict = {'LV2': '1', '_XIGUASTATE': 'XIGUASTATEID=0b8ee74b9b4d442b93a1ccc2fc37952d',
                '_XIGUA': 'UserId=43ec86f3ba207f23&Account=07565d5e3f5bb33c&checksum=773f4498a4b4',
                'ASP.NET_SessionId': 'pmbnzmnb3dhxrvn2klbmm3nh',
                'Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa': '1504411149', 'ExploreTags659938': '',
                'Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa': '1504410708', 'BigBiz659938': 'False',
                'SERVERID': '0a1db1b547a47b70726acefc0225fff8|1504413567|1504410704'}

# 直接登录后拿到的cookie, 以后需要模拟登录拿数据
cookies_str = 'ASP.NET_SessionId=pmbnzmnb3dhxrvn2klbmm3nh; _XIGUASTATE=XIGUASTATEID=0b8ee74b9b4d442b93a1ccc2fc37952d;' \
              ' Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1504410708; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=15044111' \
              '49; _XIGUA=UserId=43ec86f3ba207f23&Account=07565d5e3f5bb33c&checksum=773f4498a4b4; BigBiz659938=False;' \
              ' LV2=1; ExploreTags659938=; SERVERID=0a1db1b547a47b70726acefc0225fff8|1504413567|1504410704'


create_table_sql = "CREATE TABLE IF NOT EXISTS article_link(" \
                   "id INT PRIMARY KEY AUTO_INCREMENT," \
                   "biz VARCHAR(100)," \
                   "link varchar(300)," \
                   "title varchar(100)," \
                   "page_view INT," \
                   "thumb_number INT," \
                   "html_path VARCHAR(300),"\
                   "publish_time DATE);"

# 创建西瓜助手每个公众号主页面的链接表，对每个公众号主页面链接进行记录，对已经访问过的公众号不再访问。
create_gzh_table_sql = "CREATE TABLE IF NOT EXISTS xi_gua_gzh_link(" \
                       "id INT PRIMARY KEY AUTO_INCREMENT," \
                       "link VARCHAR(300))"

insert_gzh_sql_format = "INSERT INTO xi_gua_gzh_link(link) VALUES(\"{}\")"

select_gzh_sql_format = "SELECT * FROM xi_gua_gzh_link WHERE link = \"{}\""

insert_sql_format = "INSERT INTO article_link(biz, link, title, page_view, thumb_number) " \
             "VALUES(\"{}\", \"{}\", \"{}\", {}, {})"

select_sql_format = "SELECT * FROM article_link WHERE link = \"{}\""


def get_cookie_dict():
    strs = cookies_str.split(";")
    for string in strs:
        pos = string.index("=")
        key = string[:pos].replace(" ", "")
        value = string[pos + 1:].replace(" ", "")
        cookies_dict[key] = value
    print(cookies_dict)


def crawl_xigua():
    url = 'http://zs.xiguaji.com/MBiz/GetMBizHistory/f60d84/208837/10'
    r = requests.get(url, cookies=cookies_dict, timeout=10)
    print(r.content.__len__())


def get_gzh_links():
    """
    拿到每个公众号的URL地址，通过地址拼接，定位到相关公众号的首页。
    http://zs.xiguaji.com,这是开始地址，具体地址有这个方法得到，但是地址前面有一个#
    """
    start_page = 1
    # 这里的参数可以在主页面找到，以后要是写完整则需从主页面开始进行解析，完善爬取过程
    url = 'http://zs.xiguaji.com/MBiz/Attention/?partial=1&bizName=&tagIds=37104&page={}'
    links = []
    while 1:
        url_new = url.format(start_page)
        r = requests.get(url=url_new, cookies=cookies_dict, timeout=10)
        if r.content.__len__() < 1:
            break
        bs_obj = BeautifulSoup(r.content, "lxml")
        items = bs_obj.find_all("div", class_="item-media")
        for item in items:
            link = item.find("a").get("href")
            links.append(link)
        start_page += 1
    return links


def get_gzh_para():
    url = "http://zs.xiguaji.com"
    try:
        links = get_gzh_links()
    except BaseException as e:
        logging.error("Get WeChat Subscription link error. ErrorMsg: " + str(e))
        return
    para_dict = {}
    for link in links:
        # 注意去除地址前面的 # 号
        url_new = url + link[1:]
        try:
            r = requests.get(url_new, cookies=cookies_dict, timeout=10)
        except requests.Timeout:
            logging.error("Get content timeout. URL=" + link)
            continue
        except BaseException as e:
            logging.error("Get WeChat Subscrition homepage error. ErrorMsg: " + str(e))
            return
        bs_obj = BeautifulSoup(r.content, "lxml")
        link = bs_obj.find("a", id="btnLoadMore")
        # data_kye 和 data_id组合构成请求的路径
        data_id = link.get("data-id")
        data_key = link.get("data-key")
        para_dict[data_key] = data_id
    return para_dict


def crawl():
    try:
        date_str = datetime.datetime.now().strftime(fmt="%Y-%m-%d")
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S",
                            filename="log/" + date_str + "_log.log",
                            filemode="a")
        # create the table
        DBUtil.insert_data(create_table_sql)
        DBUtil.insert_data(create_gzh_table_sql)
        # URL中的三项分别是 data_key, data_id, page_number
        try:
            para_dict = get_gzh_para()
        except BaseException as e:
            logging.error("Get WeChat Subscription link parameter error. ErrorMsg: " + str(e))
            return
        keys = para_dict.keys()
        for key in keys:

            value = para_dict.get(key)
            result = DBUtil.select_data(select_gzh_sql_format.format(key + "/" + value))
            if result:
                continue
            try:
                crawl_gzh(key, value)
                DBUtil.insert_data(insert_gzh_sql_format.format(key + "/" + value))
            except BaseException as e:
                logging.error("Get WeChat Subscription message error. ErrorMsg: " + str(e))
    finally:
        DBUtil.close_conn()


def crawl_gzh(key, value):
    url = "http://zs.xiguaji.com/MBiz/GetMBizHistory/{}/{}/{}"
    start_page = 1
    while 1:
        new_url = url.format(key, value, start_page)
        print(new_url)
        r = requests.get(new_url, cookies=cookies_dict, timeout=10)
        if r.content.__len__() <= 20:
            break
        parse(r.content.decode("utf-8"))
        start_page += 1
        time.sleep(3)


def parse(content):
    link_pattern = re.compile(r'<a href="(http://mp.weixin.qq.com.*?)".*?>(.*?)</a>')
    view_pattern = re.compile(r'<td>(\d*)</td>[\r|\n|\s]*<td>(\d*|-.*?)</td>')
    # 返回的是一个list, 每一项是一个tuple(如果正则里面有多个括号）， 一个括号则是一个list。
    link_list = link_pattern.findall(content)
    view_list = view_pattern.findall(content)
    biz_pattern = re.compile(r'_biz=(.*?)&')
    for i in range(len(link_list)):
        link = html.unescape(link_list[i][0])
        biz = biz_pattern.findall(link)[0]
        # 注意对title都进行了转义，去掉其中的引号影响。
        title = html.escape(link_list[i][1])
        try:
            try:
                page_view = int(view_list[i][0])
            except ValueError:
                page_view = 0
            try:
                thumbs_num = int(view_list[i][1])
            except ValueError:
                thumbs_num = 0
        except:
            page_view = 0
            thumbs_num = 0
        select_sql = select_sql_format.format(link)
        result = DBUtil.select_data(select_sql)
        if not result:
            # if the link is not in the database.
            insert_sql = insert_sql_format.format(biz, link, title, page_view, thumbs_num)
            DBUtil.insert_data(insert_sql)


if __name__ == "__main__":
    crawl()



