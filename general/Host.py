from .database import create_table

class Host(object):
    """
    对爬取的每个网站的抽象, 具体的行为在子类中实现
    """
    def __init__(self):
        self.web_name = None
        self.table_name = None
        self.start_url = None
        self.pattern = None
        self.host_pattern = None
        self.general_crawl = None
        self.use_phantomjs = 0

    def get_web_name(self):
        return self.web_name

    def get_content(self, bs_obj):
        pass

    def match(self, href):
        return self.pattern.match(href)

    def get_table_name(self):
        return self.table_name

    def get_start_url(self):
        return self.start_url

    def get_parse_url(self, matcher):
        pass

    def host_match(self, url):
        return self.host_pattern.match(url)

    def save_html(self, content, url):
        pass

    def get_last_slash_pos(self, url):
        pos = 0
        while 1:
            tmp = url.find('/', pos)
            if tmp > -1:
                pos = tmp + 1
            else:
                break
        return pos

    def write(self, content, path):
        f = open(path, 'wt')
        f.write(content)
        f.close()

    def crawl(self):
        create_table(self.table_name)
        self.general_crawl.crawl(self.use_phantomjs)

    def phantomjs_condition(self, driver):
        pass