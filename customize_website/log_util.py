import logging
import datetime


class LogUtil(object):
    @staticmethod
    def log_config(level):
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        logging.basicConfig(level=level,
                            format="%(asctime)s %(filename)2[line: %(lineno)d] %(levelname)s %(message)s",
                            datefmt="%Y-%m-%d",
                            filename="log/" + date_str + "_log.log",
                            filemode="a")
