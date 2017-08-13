from selenium import webdriver

url = "http://weixin.sogou.com/weixin?query=%E6%80%9D%E7%BB%B4%E5%AF%BC%E5%9B%BE&_sug_type_=&sut=1353&lkt=1%2C1502552419169%2C1502552419169&s_from=input&_sug_=y&type=2&sst0=1502552419272&page=11&ie=utf8&w=01019900&dr=1"
key_word = "思维导图"
a = 'https://mp.weixin.qq.com/s?src=3&timestamp=1502552502&ver=1&signature=GHnvdw1eYW*GjB4fhqGObzrx043cKNx5Ja0LDgR5Ph*NzJWndEkFzsGbiOQnarTnyvqm49RA3sVrk0tbFUbiJxd2boDovfm7k52VBEO3xDJ194d9MAXBsKKSONG*L-MaEIPLtbETOS1TpwFsJV3iwq*SST4iy4-ESG9u7Qtv87Y='
b = 'https://mp.weixin.qq.com/s?src=3&amp;timestamp=1502552513&amp;ver=1&amp;signature=GHnvdw1eYW*GjB4fhqGObzrx043cKNx5Ja0LDgR5Ph*NzJWndEkFzsGbiOQnarTnyvqm49RA3sVrk0tbFUbiJxd2boDovfm7k52VBEO3xDJ194d9MAXBsKKSONG*L-MaOe43PLMCjqyuoMj6W5i-0ywlHyJFG1WDdognDe2KIrs'
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'weixin.sogou.com',
    'Referer': 'http://weixin.sogou.com/weixin?type=2&s_from=input&query=%E6%80%9D%E7%BB%B4%E5%AF%BC%E5%9B%BE%E6%A8%A1%E5%9E%8B&ie=utf8&_sug_=n&_sug_type_=',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

payload = {
    "type": "2",
    "query": key_word,
    "s_from": "input",
    "ie": 'utf8',
    '_sug_': 'n',
    '_sug_type': ''
}
driver = webdriver.PhantomJS(executable_path='/home/jfq/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
driver.get(url)
list = driver.find_elements_by_tag_name('a')
for node in list:
    print(node.get_attribute('href'))

# def get_all_link():
#     for i in