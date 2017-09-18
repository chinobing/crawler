# coding=utf-8

import requests
import re

pattern = re.compile(r"chk: \'(.*?)\'")


def login(user, password):
    data = {"email": None, "password":  None, "chk": None}
    headers = {"contentType": "application/json;charset=UTF-8", 'X-Requested-With': 'XMLHttpRequest'}

    url = 'http://zs.xiguaji.com/UserLogin?msgType=1#'
    r = requests.get(url)
    chk = pattern.findall(r.content.decode("utf-8"))
    data["email"] = user
    data["password"] = password
    data["chk"] = chk
    cookie = requests.utils.dict_from_cookiejar(r.cookies)
    r = requests.post("http://zs.xiguaji.com/Login/Login", data=str(data), headers=headers, cookies=cookie)
    cookie = dict(cookie, **requests.utils.dict_from_cookiejar(r.cookies))
    return cookie


if __name__ == "__main__":
    print(login("18911949659", "datapro123"))