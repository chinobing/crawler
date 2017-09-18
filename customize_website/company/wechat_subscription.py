# coding=utf-8

import logging
from bs4 import BeautifulSoup
import datetime

from customize_website.Crawler import Crawler
from customize_website.Util import Util


def main(run):
    if run:
        pass


class WeChatSubscription(Crawler):

    def __init__(self):
        super().__init__()
