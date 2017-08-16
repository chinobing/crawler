class Host(object):
    """
    对爬取的每个网站的抽象, 具体的行为在子类中实现
    """
    def get_web_name(self):
        pass

    def get_content(self, bs_obj):
        pass

    def match(self, href):
        pass

    def get_table_name(self):
        pass

    # def get_column(self):
    #     pass

    def get_start_url(self):
        pass

    def get_parse_url(self, href):
        pass