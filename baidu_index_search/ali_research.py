from .HostTemplate import HostTemplate
import datetime
import re


class ALi(HostTemplate):
    def __init__(self):
        super().__init__()
        self.main_page_url = "http://www.aliresearch.com"
        self.table_name = "ali_link"
        self.site = "aliresearch.com"
        self.date_format = "%Y-%m-%d"
        self.cur_date = datetime.datetime.strptime("2007-04-01", self.date_format)
        self.end_date = datetime.datetime.now()
        self.pattern = re.compile(r'(http(s)?://www.aliresearch.com)?(/blog/article/detail/id/.*?html)')
        self.max_page = 15

    def pattern_match(self, url):
        match = self.pattern.match(url)
        if match:
            return self.main_page_url + match.group(3)
        else:
            return ""
