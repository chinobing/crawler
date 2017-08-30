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
        self.cur_date = datetime.datetime.strptime("2015-04-07", self.date_format)
        self.end_date = datetime.datetime.now()
        self.pattern = re.compile(r'(http(s)?://www.cyzone.cn)?(/a/.*?html)')
        self.max_page = 5

    def pattern_match(self, url):
        match = self.pattern.match(url)
        if match:
            return self.main_page_url + match.group(3)
        else:
            return ""


class HuXiu(HostTemplate):
    def __init__(self):
        super().__init__()
        self.main_page_url = "https://www.huxiu.com"
        self.table_name = "huxiu_link"
        self.site = "huxiu.com/"
        self.date_format = "%Y-%m-%d"
        self.cur_date = datetime.datetime.strptime("2012-06-22", self.date_format)
        self.end_date = datetime.datetime.now()
        self.pattern = re.compile(r'(http(s)?://www.huxiu.com)?(/article/.*?html)')
        self.max_page = 5

    def pattern_match(self, url):
        match = self.pattern.match(url)
        if match:
            return self.main_page_url + match.group(3)
        else:
            return ""


class LeiFeng(HostTemplate):
    def __init__(self):
        super().__init__()
        self.main_page_url = "https://www.leiphone.com"
        self.table_name = "leifeng_link"
        self.site = "leiphone.com"
        self.date_format = "%Y-%m-%d"
        self.cur_date = datetime.datetime.strptime("2011-01-01", self.date_format)
        self.end_date = datetime.datetime.now()
        self.pattern = re.compile(r'(http(s)?://www.leiphone.com)?(/.*?html)')
        self.max_page = 5

    def pattern_match(self, url):
        match = self.pattern.match(url)
        if match:
            return self.main_page_url + match.group(3)
        else:
            return ""


class TouZiJie(HostTemplate):
    def __init__(self):
        super().__init__()
        self.main_page_url = "http://www.pedaily.cn"
        self.table_name = "touzijie_link"
        self.site = "pedaily.cn"
        self.date_format = "%Y-%m-%d"
        self.cur_date = datetime.datetime.strptime("2010-01-01", self.date_format)
        self.end_date = datetime.datetime.now()
        self.pattern = re.compile(r'(http(s)?://.*?.pedaily.cn)?(/.*?html)')
        self.max_page = 5

    def pattern_match(self, url):
        match = self.pattern.match(url)
        if match:
            return self.main_page_url + match.group(3)
        else:
            return ""