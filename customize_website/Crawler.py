# coding=utf-8

import logging


class Crawler(object):
    """
    针对每个网站的每个栏目,都需要继承这个类.
    此类抽象了整个过程,实现每个方法就可以了.
    """
    def __init__(self):
        self.item_path = None
        self.dirs = None

    def crawl(self):
        pass

    def get_link_data(self):
        pass

    def insert_link(self, ):
        pass

    def make_dirs(self):
        pass

    def save_html_file(self):
        pass

    def save_content_file(self):
        pass
