# coding=utf-8
import logging
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Crawler(object):

    all_file_dir = "/home/jfq/Documents/datapro_html/"

    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 修改userAgent 以及不加载图片
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")  # 设置user-agent请求头
    dcap["phantomjs.page.settings.loadImages"] = False

    cookie_dict = {
        "name": None,
        "value": None,
        "domain": None,
        "path": "/",
        # "expire": None
    }

    """
    针对每个网站的每个栏目,都需要继承这个类.
    此类抽象了整个过程,实现每个方法就可以了.
    """
    def __init__(self):
        self.tag_file_path = "/home/jfq/36kr_with_tag.csv"

    def crawl(self):
        """
        爬取所有链接的方法
        :return:
        """
        pass

    def get_link_data(self, item_dict):
        try:
            html_content = self.use_phantom_get_req(item_dict['link'])
            tags = self.parse_html(html_content)  # tags包含所有的tag, 用--分隔
            content = str(item_dict['id']) + "," + item_dict["link"] + ","\
                + item_dict["title"] + "," + item_dict['html_path'].replace("html", "txt")\
                + "," + tags + "\n"
            self.save_content_file(content)
        except BaseException as e:
            logging.error("Process link failed. URL=%s, ErrorMsg: %s" % (item_dict['link'], str(e)))
            raise BaseException

    def parse_html(self, content):
        """
        :return: 链接所在的正文, 转义所有的换行符为\n
        """
        return ""

    def save_content_file(self, content):
        # 保存带有标签的数据到文本中,以csv格式保存
        try:
            f = open(self.tag_file_path, 'at', encoding="utf-8")
            f.write(content)
        except BaseException as e:
            logging.error("Save content file error. ErrorMsg: %s" % str(e))
            raise BaseException()
        finally:
            f.close()

    def use_phantom_get_req(self, url):
        try:
            driver = webdriver.PhantomJS(
                executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',
                desired_capabilities=Crawler.dcap)

            driver.set_page_load_timeout(30)
            driver.get(url)
            logging.info("Get %s success." % url)
            return driver.page_source
        except BaseException as e:
            logging.error("Get link error. ErrorMsg: %s" % str(e))
        finally:
            driver.quit()
