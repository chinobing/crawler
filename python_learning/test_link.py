import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re

def phantomjs():
    driver = webdriver.PhantomJS(executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    desired_capabilities["phantomjs.page.settings.loadImages"] = False
    driver = webdriver.PhantomJS(
        executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.start_session(desired_capabilities)
    driver.set_page_load_timeout(20)

    driver.get('http://www.tmtpost.com')
    driver.implicitly_wait(30)
    driver.find_element_by_class_name('load_more').click()
    bs_obj = BeautifulSoup(driver.page_source.encode('utf-8'), 'lxml')
    link_list = bs_obj.find_all('a')
    for link in link_list:
        print(link.get('href'))

cookies_str = 'pgv_pvi=6058293248; UM_distinctid=15df81c9c2d822-03fea8eb1c727e-317d0258-1fa400-15df81c9c2f6b0; pgv_si=s6963487744; acw_tc=AQAAAH4hsjX91Q0Aqv2Bt/168T3kzg86; responseTimeline=1033; lastest_num=24; ci_session=627775dd0bdcafa824c7e25e5022fc7d055a61bd; CNZZDATA5193056=cnzz_eid%3D1796870796-1503105281-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1503566437; _ga=GA1.2.1351578126.1503106211; _gid=GA1.2.512628594.1503557372; trctestcookie=ok; zg_did=%7B%22did%22%3A%20%2215df81ca26b545-0c45eb1941d89f-317d0258-1fa400-15df81ca26c8d1%22%7D; zg_dc1e574e14aa4c44b51282dca03c46f4=%7B%22sid%22%3A%201503567657.167%2C%22updated%22%3A%201503568956.605%2C%22info%22%3A%201503106212470%7D; Hm_lvt_c2faa2e59b5c08b979ccf8a901af64a8=1503557372,1503561074,1503561186,1503565077; Hm_lpvt_c2faa2e59b5c08b979ccf8a901af64a8=1503568957; trc_cookie_storage=taboola%2520global%253Auser-id%3Da0a97637-cd82-46e0-b16c-49e7eeb7855a-tuct4f4899'


def split_cookie(cookies_strs):
    cookies = {}
    cookies_arr = cookies_strs.split(';')
    pattern = re.compile(r"(.*?)=(.*)")
    for strs in cookies_arr:
        matcher = pattern.match(strs)
        if matcher:
            cookies[matcher.group(1)] = matcher.group(2)
    return cookies


def post():
    param = {
        'url': "/v1/lists/home",
        'data': 'offset=90&limit=15&post_fields=tags,access&tag_special_background_image_size=["640_256"]&auction_background_image_size=["640_256"]&ad_image_size=["640_256"]&focus_post_image_size=["640_256"]&homepage_universal_article_group_image_size=["210_240"]&special_column_post_image_size=["210_240"]&homepage_tag_group_image_size=["210_240"]&homepage_author_group_image_size=["210_240"]&thumb_image_size=["200_150"]'
    }
    r = requests.get(url="http://www.tmtpost.com/2737260.html")
    cookies = r.cookies
    print(cookies)
    r1 = requests.post('http://www.tmtpost.com/ajax/common/get', data=param, cookies=split_cookie(cookies_str))
    print(r1.text)


if __name__ == "__main__":
    r = requests.get("http://www.baidu.com/s?ie=UTF-8&wd=2017-03-04%20site%3A199it.com")
    print(r.content.decode('gb2312'))
