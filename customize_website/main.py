import logging
import datetime
from customize_website import xin_lang_ke_ji


def main():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename="log/" + date_str + ".log",
                        filemode="a")
    xin_lang_ke_ji.main()


if __name__ == "__main__":
    main()

