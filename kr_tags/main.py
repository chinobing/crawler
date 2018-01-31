import datetime
import logging

from .san_shi_liu_ke import main as kr_main
from .database import DBUtil


def main():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    terminal_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("log/" + date_str + ".log", "a")
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=[terminal_handler, file_handler])
    kr_main(1)

if __name__ == "__main__":
    try:
        main()
    finally:
        DBUtil.close_conn()    # 最后一定要关闭资源.
