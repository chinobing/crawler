from general.kr import crawl_data
import re
from general.ali import *
from general.company.tai_mei_ti import TaiMeiTi
from general.yiguan import *
from general.general_crawler import *
import time
from baidu_index_search.tai_mei_ti import TaiMeiTi
from baidu_index_search import Company

# crawl_data()

# pattern = re.compile(r'(http(s)?://36kr\.com)?(/p/.*?html)')
# s = 'http://36kr.com/p/1234.html#dafds123'
# mt = pattern.match(s)
# if mt:
#     print(mt.group(3))
# host = ALi()
# host = YiGuan()
# crawler = GeneralCrawler(host)
# crawler.crawl()

# save_simple_url()

obj = Company.LeiFeng()
obj.crawl_link()
