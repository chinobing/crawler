from .HostTemplate import HostTemplate
import datetime
import re


class YiGuan(HostTemplate):
    def __init__(self):
        super().__init__()
        self.main_page_url = "http://www.199it.com"
        self.table_name = "yiguan_link"
        self.site = "199it.com"
        self.date_format = "%Y-%m-%d"
        self.cur_date = datetime.datetime.strptime("2017-03-26", self.date_format)
        self.end_date = datetime.datetime.now()
        self.pattern = re.compile(r'(http(s)?://www.199it.com)?(/archives/.*?html)')
        self.max_page = 5

    def pattern_match(self, url):
        match = self.pattern.match(url)
        if match:
            return self.main_page_url + match.group(3)
        else:
            return ""
