import re
import requests
from urllib import parse
from lxml import etree


def get_location(url):
    """通过百度的url拿到目标url"""
    r = requests.get(url, allow_redirects=False)
    try:
        location = r.headers["Location"]
    except Exception as e:
        location = ""
    return location


def get_info(key_word, site):
    max_page = 10
    key_word_quote = parse.quote(key_word)
    url = str.format('http://www.baidu.com/s?ie=UTF-8&wd={}%20site%3A{}', key_word_quote, site)
    # result = []
    failure = 0
    count = 0
    while len(url) > 0 and failure < 10:

        try:
            r = requests.get(url, timeout=10)
        except Exception as e:
            failure += 1
            continue

        if r.status_code == 200:

            hrefs = list(set(re.findall('"(http://www\\.baidu\\.com/link\\?url=.*?)"', r.content.decode('utf-8'))))
            for href in hrefs:
                print(href + ": " + get_location(href))
                print(count)
                count += 1
            # result += hrefs
            tree = etree.HTML(r.content)
            next_page_text = tree.xpath(
                '//div[@id="page"]/a[@class="n" and contains(text(), "下一页")]/@href')

            url = 'http://www.baidu.com' + next_page_text[0].strip() if next_page_text else ''
            failure = 0
            max_page -= 1
            if max_page <= 0:
                break
        else:
            failure += 2
            print('search failed: %s' % r.status_code)
    if failure >= 10:
        print('search failed: %s' % url)

if __name__ == "__main__":
    get_info('2017-08-24', 'tmtpost.com')
    # url = 'http://www.baidu.com/link?url=URttQvJm_h-kMp-aw7WzvRzEvexC_Ev48R6nfCIzYCrBESrfeAc_kHTXJjgFYviT'
    # r = requests.get(url, allow_redirects=False)
    # print(r.headers['Location'])