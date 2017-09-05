a = "http:www.cc.com/hello/world/a.html"
pos = -1
while 1:
    pos = a.find("/", pos + 1)
    if pos < 0:
        break
    print(pos)
print(pos)