from lagou.lagouspider import *
from lagou.header import zixun_company
from lagou.spider_test import *


keys = zixun_company.keys()

for key in keys:
    print(key)
    get_data(key, zixun_company[key])

