import requests
from bs4 import BeautifulSoup

start_url = 'http://www.199it.com/'
content_url = 'http://www.199it.com/archives/622174.html'


r = requests.get(content_url)
bs_obj = BeautifulSoup(r.content, "lxml")
links = bs_obj.find_all('a')
for link in links:
    print(link.get('href'))
