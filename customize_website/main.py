import logging
import datetime
from customize_website import xin_lang_ke_ji
from customize_website import feng_huang_chuang_xin
from customize_website.database import DBUtil

def main():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    terminal_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("log/" + date_str + ".log", "a")
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        # filename="log/" + date_str + ".log",
                        # filemode="a",
                        handlers=[terminal_handler, file_handler])
    DBUtil.create_table()
    # xin_lang_ke_ji.main()
    feng_huang_chuang_xin.main()

if __name__ == "__main__":
    main()

