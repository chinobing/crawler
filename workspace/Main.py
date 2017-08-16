import  requests


r = requests.get("https://www.analysys.cn/analysis/8/detail/1000843/")
print(r.text)