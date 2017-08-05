from scrapy.spiders import BaseSpider
from scrapy.http.request import Request
from .Util import *


class DmozSpider(BaseSpider):
    name = "lg"
    allowed_domain = ["lagou.com"]
    start_urls = [
        "https://www.lagou.com/zhaopin/"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response):
        # print(response.body)
        for sel in response.xpath('//*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/a/h3'):
           print(sel.xpath("text()").extract())
