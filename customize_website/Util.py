# coding=utf-8
import logging

class Util(object):

    @staticmethod
    def all_strip(s):
        """
        remove all '\r' '\n' ' ' 
        删除一个字符串中所有的上述字符
        :return: 
        """
        try:
            return s.replace("\r", "").replace("\n", "").replace(" ", "")
        except BaseException as e:
            logging.error("Replace \\r\\n\\S failed! ErrorMsg: %s" % str(e))
            return ""

    @staticmethod
    def get_content_from_tag(content_tag):
        [script.extract() for script in content_tag.findAll("script")]
        [style.extract() for style in content_tag.findAll("style")]
        return content_tag.get_text()
