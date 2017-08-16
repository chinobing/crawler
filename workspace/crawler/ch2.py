from urllib.request import urlopen
from bs4 import BeautifulSoup


def code_1():
    html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
    bs_obj = BeautifulSoup(html, 'lxml')
    name_list = bs_obj.find_all()
    for name in name_list:
        print(name.get_text())


if __name__ == '__main__':

    code_1()