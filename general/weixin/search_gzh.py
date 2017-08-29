import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
import time

url_format = 'http://weixin.sogou.com/weixin?query=%E8%B5%84%E6%9C%AC&_sug_type_=&s_from=input&_sug_=n&type=1&page={}&ie=utf8'
jijin_url_format = 'http://weixin.sogou.com/weixin?hp=36&query=%E5%9F%BA%E9%87%91&sut=3286&lkt=1%2C1503128964386%2C1503128964386&_sug_=y&sst0=1503128964507&oq=&stj0=0&stj1=4&hp1=&stj2=0&stj=0%3B4%3B0%3B0&_sug_type_=&ri=1&s_from=input&type=1&page={}&ie=utf8&w=01015002&dr=1'
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'SUV=00504AE3B781FDAA596A17A1BAF22354; ABTEST=0|1502551483|v1; IPLOC=CN3301; SUID=AAFD81B74A42910A00000000598F1DBB; SUID=AAFD81B75218910A00000000598F1DBC; weixinIndexVisited=1; ppinf=5|1502555579|1503765179|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozOmpmcXxjcnQ6MTA6MTUwMjU1NTU3OXxyZWZuaWNrOjM6amZxfHVzZXJpZDo0NDpvOXQybHVOVkkxc2ozamxScmVtWUg1Q2Y4R3NjQHdlaXhpbi5zb2h1LmNvbXw; pprdig=k8mbzjWktHHpevaVWpy2MTczEenaCeP_rnLcisWx_kjxcfOeKWv3p6-dlBQiJ7dbBI7Es5028KHfz4RO5DENPM9jrY3zVaz5UH6XtRYdIRTfJlSD6Iu19vhDkswvdJ79OYVpHEAQ594HwD_74dKCuxvuumKcgYL5RBM2OELueQw; sgid=23-30272119-AVmPLbtib2udkXocFeYbCM2U; sw_uuid=4035241682; ssuid=596381032; dt_ssuid=5662230140; SNUID=CE98E4D36460329678ED1806654065AF; JSESSIONID=aaalPOOSXIMmc__jF5U3v; pgv_pvi=6406982656; pgv_si=s958265344; ppmdig=15031220820000007d38fa57b6c75039f1c40e670b38e61d; sct=17',
    'Host': 'weixin.sogou.com',
    'Referer': 'http://weixin.sogou.com/weixin?query=%E8%B5%84%E6%9C%AC&_sug_type_=&s_from=input&_sug_=n&type=1&page=16&ie=utf8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}
domain = ".sogou.com"
cookie = {

    'SUV': '00504AE3B781FDAA596A17A1BAF22354',
    'ABTEST': '0|1502551483|v1',
    'IPLOC': 'CN3301',
    'SUID': 'AAFD81B74A42910A00000000598F1DBB',
    'weixinIndexVisited': '1',
    'ppinf': '5|1502555579|1503765179|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozOmpmcXxjcnQ6MTA6MTUwMjU1NTU3OXxyZWZuaWNrOjM6amZxfHVzZXJpZDo0NDpvOXQybHVOVkkxc2ozamxScmVtWUg1Q2Y4R3NjQHdlaXhpbi5zb2h1LmNvbXw',
    'pprdig': 'k8mbzjWktHHpevaVWpy2MTczEenaCeP_rnLcisWx_kjxcfOeKWv3p6-dlBQiJ7dbBI7Es5028KHfz4RO5DENPM9jrY3zVaz5UH6XtRYdIRTfJlSD6Iu19vhDkswvdJ79OYVpHEAQ594HwD_74dKCuxvuumKcgYL5RBM2OELueQw',
    'sgid': '23-30272119-AVmPLbtib2udkXocFeYbCM2U', 'sw_uuid': '4035241682', 'ssuid': '596381032',
    'dt_ssuid': '5662230140', 'SNUID': 'CE98E4D36460329678ED1806654065AF', 'JSESSIONID': 'aaalPOOSXIMmc__jF5U3v',
    'pgv_pvi': '6406982656', 'pgv_si': 's958265344', 'ppmdig': '15031220820000007d38fa57b6c75039f1c40e670b38e61d',
    'sct': '17'
}

proxy = ['60.178.131.183:8081']


def parse(tag):
    info = get_wein_xin_account_and_articles(tag)
    if info:
        info.replace("\n", '-')
    name, link = get_account_name_and_link(tag)
    func_desc = get_function_desc(tag)
    company = get_company(tag)
    article_link, article_title = get_latest_article(tag)
    return name.replace("\n", '') + ',' + link.replace("\n", '') + ',' + info + ',' + func_desc.replace("\n", '') \
           + ',' + company.replace("\n", '') + ',' + article_title.replace("\n", '') + "," + article_link.replace("\n", '')


def get_account_name_and_link(tag):
    try:
        tag_a = tag.find("a", {"uigs": re.compile('account_name_\d*')})
        link = tag_a.get('href')
        name = tag_a.get_text()
        return name, link
    except:
        return '', ''


def get_wein_xin_account_and_articles(tag):
    try:
        name = tag.find('p', class_='info').get_text()
        return name
    except:
        return ''


def get_function_desc(tag):
    try:
        func = tag.find(text='功能介绍：')
        func_desc = func.parent.parent.find('dd').get_text()
        return func_desc
    except:
        return ''


def get_company(tag):
    try:
        company = tag.find(text='微信认证：')
        com_desc = company.parent.parent.find('dd').get_text()
        return com_desc
    except:
        return ''


def get_latest_article(tag):
    try:
        article = tag.find(text="最近文章：")
        link = article.parent.parent.find('a')
        return link.get('href'), link.get_text()
    except:
        return '', ''


def crawl(content, page=1):
    # r = requests.get(str.format(jijin_url_format, page), headers=header)
    bs_obj = BeautifulSoup(content, 'lxml')
    user_accounts = bs_obj.find_all('li', {"id": re.compile(r"sogou_vr_11002301_box_\d*")})
    for node in user_accounts:
        store_data(parse(node))


def get_content(page):
    try:
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities["phantomjs.page.settings.userAgent"] = header['User-Agent']
        # desired_capabilities["phantomjs.page.settings.loadImages"] = False
        # proxy_add = webdriver.Proxy()
        # proxy_add.proxy_type = ProxyType.MANUAL
        # proxy_add.http_proxy = proxy[0]
        # proxy_add.add_to_capabilities(desired_capabilities)
        driver = webdriver.PhantomJS(
            executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        driver.start_session(desired_capabilities)
        # driver.get("http://weixin.sogou.com")
        # driver.delete_all_cookies()
        keys = cookie.keys()
        for key in keys:
            driver.add_cookie({'name': key, 'value': cookie[key], 'domain': domain, 'path': "/"})
        driver.get(str.format(jijin_url_format, page))
        content = driver.page_source.encode('utf-8')
        return content
    finally:
        driver.quit()


def store_data(data):
    print(data)
    f = open("./jijin.csv", 'at')
    f.write(data.replace("\n", ""))
    f.write('\n')
    f.close()


def write_header():
    f = open("./jijin.csv", 'at')
    header = '公众号名称,链接,基本信息,介绍,最近文章,文章链接\n'
    f.write(header)
    f.close()

if __name__ == "__main__":
    for i in range(14, 20):
        content = get_content(i)
        crawl(content=content, page=i)
        time.sleep(30)



