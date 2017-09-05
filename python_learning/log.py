import logging
import python_learning.log_file as log_file

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="log.log",
                    filemode="a")


def h():
    logging.info("method h start")
    logging.info("method h enc")


class InFile(object):

    def f(self):
        logging.info("InFile instance f starts")
        logging.info("Infile instance f ends")

    @staticmethod
    def g():
        logging.info("InFile instance g starts")
        logging.info("Infile instance g ends")


if __name__ == "__main__":
    log_file.f()
    test = log_file.TestLog()
    test.g(123)
    log_file.TestLog.f()
    h()
    test_in = InFile()
    test_in.f()
    InFile.g()