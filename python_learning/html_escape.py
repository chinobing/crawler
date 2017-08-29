from html.parser import unescape

url = "http:\\/\\/mp.weixin.qq.com\\/s?__biz=MjAzNzMzNTkyMQ==&amp;mid=2653763979&amp;idx=2&amp;sn=de10ded2b68b5e5f0d8fa1c4e7909e25&amp;chksm=4a8929957dfea083d27da8a0ad9509d5ac14c2920099facf2bf7e8ae2e37f4cb2f2551488a37&amp;scene=27#wechat_redirect"
url_new = unescape(url).replace("\\","")
print(url_new)
