import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector


class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://dmoztools.net/Computers/Programming/Languages/Python/Books/",
        "http://dmoztools.net/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        hxs = scrapy.Selector(response)
        sites = hxs.path("//fieldset/ul/ui")
        for site in sites:
            title = site.path('a/text()').extract()
            link = site.path('a/@href').extract()
            desc = site.path('text()').extract()
            print(title + ":  " + link)
