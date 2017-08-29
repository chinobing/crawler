from .HostTemplate import HostTemplate
import datetime
import re


class Kr(HostTemplate):
    def __init__(self):
        super().__init__()
        self.main_page_url = "http://www.36kr.com"
        self.table_name = "36kr_link"
        self.site = "36kr.com"
        self.date_format = "%Y-%m-%d"
        self.cur_date = datetime.datetime.strptime("2011-08-01", self.date_format)
        self.end_date = datetime.datetime.now()
        self.pattern = re.compile(r'(http(s)?://(www\.)?36kr\.com)?(/p/[^/]*html)')  # 对站点过滤的正则表达式 (re pattern)
        self.max_page = 15

    def pattern_match(self, url):
        match = self.pattern.match(url)
        if match:
            return self.main_page_url + match.group(4)
        else:
            return ""
