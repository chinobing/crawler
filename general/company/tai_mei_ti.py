from ..Host import Host
import re
from ..general_crawler import GeneralCrawler
from ..database import create_table

class TaiMeiTi(Host):
    def __init__(self):
        super().__init__()
        self.web_name = "tai_mei_ti"
        self.table_name = "taimeiti_link"
        self.start_url = "http://www.tmtpost.com"
        self.pattern = re.compile(r'(http(s)?://www.tmtpost.com)?(/[^/]*html)')
        self.host_pattern = re.compile(r'http(s)?://www.tmtpost.com')
        self.general_crawl = GeneralCrawler(host=self)
        self.use_phantomjs = 1

    def get_parse_url(self, matcher):
        return self.start_url + matcher.group(3)

    # 针对有特殊加载需要的页面,只有等到加载完后
    def phantomjs_condition(self, driver):
        driver.implicitly_wait(20)
        driver.find_element_by_class_name('trc_rbox_container')
