from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from copy import deepcopy

def set_cookie():
    try:
        driver = webdriver.PhantomJS(executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        desi_capa = driver.desired_capabilities.copy()
        desi_capa['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        driver.start_session(desi_capa)
        driver.get("https://www.baidu.com")
        print(driver.get_cookies())
        driver.add_cookie({'name': 'token', 'value': '1234', 'domain': '.baidu.com', "expire": None, 'path': '/'})
        print("success")
    finally:
        driver.quit()


cookies = {
  	"sid": '123',
    "uid": '456',
    'jsession': 'dadaf12dfafs'
}
domain = '.baicu.com'
cookie_dict = {
        "name": None,
        "value": None,
        "domain": domain,
        "path": "/",
        # "expire": None
}


def set_multi_cookies():
    try:
        driver = webdriver.PhantomJS(executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        keys = cookies.keys()
        for key in keys:
            cookie_dict_ins = deepcopy(cookie_dict)
            cookie_dict_ins['name'] = key
            cookie_dict_ins['value'] = cookies[key]
            driver.add_cookie(cookie_dict_ins)
        print(driver.get_cookies())
    finally:
        driver.quit()


if __name__ == "__main__":
    set_cookie()
