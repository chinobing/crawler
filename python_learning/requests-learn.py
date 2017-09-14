import requests
import html.parser
import re

url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=402&lid=2559&num=20&versionNumber=1.2.8&page=39&encode=utf-8&callback=feedCardJsonpCallback&_=1505372676381'

r = requests.get(url)
link_set = set()
pattern = re.compile(r'(http:[^,]*?\.s?html?)')
links = pattern.findall(html.parser.HTMLParser().unescape(r.content.decode("utf-8")))

for link in links:
    url = link.replace("\\", "")
    pos = url.rfind("/")
    if not url[pos:] in link_set:
        link_set.add(url[pos:])
        print(url)

