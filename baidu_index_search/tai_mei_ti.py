from .HostTemplate import HostTemplate
import datetime
import re


class TaiMeiTi(HostTemplate):
    def __init__(self):
        super().__init__()
        self.main_page_url = "http://www.tmtpost.com"
        self.table_name = "taimeiti_link"
        self.site = "tmtpost.com"
        self.date_format = "%Y-%m-%d"
        self.cur_date = datetime.datetime.strptime("2017-06-17", self.date_format)
        self.end_date = datetime.datetime.now()
        self.pattern = re.compile(r'(http(s)?://www\.tmtpost\.com)?(/[^/]*html)')  # 对站点过滤的正则表达式 (re pattern)
        self.max_page = 15

    def pattern_match(self, url):
        match = self.pattern.match(url)
        if match:
            return self.main_page_url + match.group(3)
        else:
            return ""
