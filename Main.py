from lagou.lagouspider import *
from lagou.header import caijing_school_1

keys = caijing_school_1.keys()

for key in keys:
    print(key)
    get_data(key, caijing_school_1[key])
