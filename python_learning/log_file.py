import logging


def f():
    logging.info("function f starts.")
    print("hello world")
    logging.info("function f ends")


class TestLog(object):

    def g(self, i):
        logging.info("TestLog instance invoke g")
        print(i)
        logging.info("TestLog instance invoke g finished.")

    @staticmethod
    def f():
        logging.info("TestLog static method f starts.")
        print("Static method f")
        logging.info("TestLog static method g f end")