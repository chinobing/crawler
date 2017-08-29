import re


def start_re():
    pattern = re.compile("http://www.baidu.com|^/")
    url = "/img/1.jpg"
    url_with_http = "http://www.baidu.com/1/s/1.html"
    matcher = pattern.match(url)
    if matcher:
        print(url)
    matcher = pattern.match(url_with_http)
    if matcher:
        print(url_with_http)


def re_replace():
    url = '/mp/profile_ext?action=getmsg&__biz=MjAzNzMzNTkyMQ==&f=json&offset=2000&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=qbXFpMD7b%2BKwLH1DPo1Lj%2BOoemIoMZiOSbBSnCMyIjAI0e0GUJCaFRokbBA%2B3iQw&wxtoken=&appmsg_token=919_9khp59t5aSWHM%2FrSlPWwiogG8hBa_uzxA4vsOQ~~&x5=1&f=json'
    pattern = re.compile(r".*?\?(.*)")
    match = pattern.match(url)
    msg = ""
    if match:
        para = match.group(1)
        offset_index = para.index("offset=") + 7
        amp_index = para.index("&", offset_index)
        page = int(para[offset_index: amp_index]) + 10
        para = para[0: offset_index] + str(page) + para[amp_index:]
        msg = "http://mp.weixin.qq.com/mp/profile_ext?" + para
    print(msg)


if __name__ == "__main__":
    re_replace()
