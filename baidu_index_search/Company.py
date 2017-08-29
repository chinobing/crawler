from .HostTemplate import HostTemplate
import datetime
import re


class ChuangYeBang(HostTemplate):
    def __init__(self):
        super().__init__()
        self.main_page_url = "http://http://www.cyzone.cn"
        self.table_name = "chuangyebang_link"
        self.site = "cyzone.cn"
        self.date_format = "%Y-%m-%d"
        self.cur_date = datetime.datetime.strptime("2008-01-01", self.date_format)
        self.end_date = datetime.datetime.now()
        self.pattern = re.compile(r'(http(s)?://www.cyzone.cn)?(/a/.*?html)')
        self.max_page = 5

    def pattern_match(self, url):
        match = self.pattern.match(url)
        if match:
            return self.main_page_url + match.group(3)
        else:
            return ""
