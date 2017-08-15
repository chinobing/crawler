import requests
from bs4 import BeautifulSoup

start_url = "https://www.mckinsey.com.cn/"

r = requests.get(start_url)
bs_obj = BeautifulSoup(r.content, "lxml")
links = bs_obj.find_all('a')
for link in links:
    print(link.get('href'))