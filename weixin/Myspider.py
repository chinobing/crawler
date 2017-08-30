#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from bs4 import BeautifulSoup
from urllib import request
import chardet
import os
import gzip
import threading
import _thread
import socket
from CxExtractor import CxExtractor

cx = CxExtractor(threshold=186)
# 这是一个基于urllib实现全网爬取的多线程爬虫
# Create by Jack

# 想要抓取的关键字列表
keywords = ['微博搞笑排行榜']
keycode = ''
for key in keywords:
    keycode += key
keycode = request.quote(keycode)
urls = [
    'http://weixin.sogou.com/weixin?type=1&s_from=input&quer=' + keycode,
    # 'https://www.baidu.com/s?wd='+keycode,
    # 'http://weixin.sogou.com/weixin?type=2&query='+keycode,
    # 'http://zhihu.sogou.com/zhihu?query='+keycode
]


# 入口url列表
def getContent(url):
    html = cx.getHtml(url)
    content = cx.filter_tags(html)
    s = cx.getText(content)
    return s


# 用一个递增的数字作为文件名标识
counter = 0
# 互斥锁，用于线程对互斥资源的访问
mutex = threading.Lock()


def findEnd(values, k=5):
    """
    @:param values	正文段列表
    k 		每次选取的段数
    @:return left	正文起始段
    right	正文结束段
    """
    left, right = 0, 0
    # print(values)
    for i in range(len(values)):
        strCnt = sum(values[i:i + k])
        # print(strCnt)
        if strCnt > 180 and values[i] > 15:
            if left == 0:
                left = i
            right = i
    cnt = 0
    for i in range(right, len(values)):
        if cnt >= k:
            break
        if values[i] > 15:
            right += 1
        cnt += 1
    return left, right


def filt(content, k=1):
    """
    找出正文的起始位置和结束位置
    @:param content	过滤标签后的网页
    k 		每段选取的行数
    @:return left	正文起始段
    right	正文结束段
    """
    if not content:
        return None, None
    lines = content.split('\n')
    group_value = []
    for i in range(0, len(lines), k):
        group = '\n'.join(lines[i:i + k]).strip()
        group_value.append(len(group))
    left, right = findEnd(group_value)
    return left, right


def extract(content):
    """
    基于正文提取算法（行快分布）实现的提取函数
    @param: content	过滤标签后的网页
    @return:res		正文
    """
    if content.count('\n') < 10:
        # 如果换行符少于10，则认为html是经过压缩的，进行换行处理
        content = content.replace('>\n', '\n')
    content = tool.replace(content)
    left, right = filt(content)
    return '\n'.join(content.split('\n')[left:right])


def extractForAilab(content):
    """
    为特殊网页结构而特别设计的提取函数
    @:param content	过滤标签后的网页
    @:return 正文
    """
    try:
        # tool.save(''.join(content.split('\n'))+'\n\n\n','a','haha')
        soup = BeautifulSoup(content, 'html.parser')
        main = soup.find(attrs={'id': 'mainDiv'})
        [s.extract() for s in main(['div'])]
        s = main.get_text()
        r = re.compile(r'<[^>]+>', re.M | re.S)
        s = r.sub('', s).strip()  # 删除HTML标签
        r = re.compile(r'^\s+$', re.M | re.S)  # 删除空白行
        s = r.sub('', s)
        r = re.compile(r'\n+', re.M | re.S)  # 合并空行为一行
        s = r.sub('\n', s)
        return s
    except Exception as e:
        print(e)
        return ''


def loop(url):
    """
    子线程抓取页面，并以文本文件的方式将其存到本地磁盘中
    :param url: 	当前要抓取的页面
    :return: 
    """
    try:
        global counter, mutex
        print('fetching %s...' % url)
        if str(url).startswith("https://www.baidu.com/s?wd=") or len(url) > 400:
            print('dropfetching %s...' % url)
            return
        page = tool.fetchPage(url)
        if page == '':
            print('droppage:%s' % url)
            tool.save(url + '\n', 'a', 'dropedUrls')
            return
        r = re.compile(r'<title>(.*?)</title>', re.M | re.S)
        title = ''.join(re.findall(r, page))
        if spider.getHost(url) == 'http://www.ailab.cn':
            body = extractForAilab(page)
        else:
            body = extract(page)
        if body == '' or len(body) < 50:  # 使用另一种算法再次抽取
            content = getContent(url)
            if content == '' or len(content) < 50:
                print('drop:%s' % url)
                tool.save(url + '\n', 'a', 'dropedUrls')
            else:
                if mutex.acquire():  # 互斥锁
                    counter += 1
                    tool.save(content, name=str(counter))
                    print('successByAlgorithm2:%s' % url)
                    mutex.release()
        else:
            if mutex.acquire():  # 互斥锁
                counter += 1
                tool.save('标题：' + title + '\n\n' + body, name=str(counter))
                print('success:%s' % url)
                mutex.release()
    except:
        print('loop error')
        return ''


class MySpider:
    def __init__(self, urls):
        self.cur_depth = 0
        self.queue = MyQueue()
        tool.remove('urls')
        tool.remove('important')
        tool.remove('dropedUrls')
        self.url_dict = dict()
        if isinstance(urls, str):
            self.queue.addUnvisitedUrl(urls, 1)
            self.url_dict[urls] = 1
        elif isinstance(urls, list):
            for url in urls:
                self.queue.addUnvisitedUrl(url, 1)
                self.url_dict[url] = 1

    def crawl(self, depth):
        """
        通过bfs进行搜索爬取感兴趣的页面
        @:param depth 	爬取的深度
        """
        queue = self.queue
        for i in range(depth):
            unvisted_links = []
            while not queue.isUnvisitedEmpty():
                try:
                    cur_url = queue.unVisitedDequeue()
                    print('pop link:%s' % cur_url)
                    links = []
                    if cur_url is not None and cur_url != '':
                        links = self.fetchLinks(cur_url)
                    unvisted_links.extend(links)
                    print('get %d new links' % len(links))
                    queue.addVisitedUrl(cur_url)
                    print('visited count:%d' % queue.getVisitedNums())
                    print('current depth:%d' % (i + 1))
                except:
                    print('crawl error')
                    continue
            if len(unvisted_links) > 0:
                for link in unvisted_links:
                    level = self.url_dict[link]
                    queue.addUnvisitedUrl(link, level)
            else:
                break
            print('unVisited count:%d' % queue.getunVisitedNums())

    def fetchLinks(self, url):
        """
        解析当前页面中的全部url连接，抓取感兴趣的页面，并将过滤后的url列表加入待爬取队列中
        这里用了一个简单的思想：1. 如果当前页面中的子页面是我们感兴趣的，则认为这个页面是重要的
                            2. 如果当前页面中我们感兴趣的子页面超过10个，则认为这个页面也是重要的
        @:param depth 	爬取的深度
        """
        links = []
        page = tool.fetchPage(url)
        page_num = 0
        url_dict = self.url_dict
        if page != '':
            try:
                soup = BeautifulSoup(page, 'html.parser')
                items = soup.findAll('a')
                for item in items:
                    link = item.get('href')
                    guanggao = item.get('data-is-main-url')
                    if 'true' == guanggao:
                        pass
                    else:
                        title = item.get_text()
                        newlink = ''
                        pageType = 0
                        if link != None and link != '' and len(link) > 3 and 'javascript' not in link:
                            for k in keywords:
                                if k in title:
                                    pageType = 1
                                    break
                            if link[:4] != 'http':
                                host = self.getHost(url)
                                if link[0] in ['/', '?']:
                                    newlink = host + link
                                else:
                                    newlink = host + '/' + link
                            elif link[:4] == 'http':
                                newlink = link
                            if link != '':
                                if newlink not in url_dict:
                                    links.append(newlink)
                                    tool.save(link + '\n', option='a', name='urls')
                                    if pageType == 1:
                                        _thread.start_new_thread(loop, (newlink,))
                                        page_num += 1
            except:
                print('extract error')
                return []

        if page_num >= 10:  # 当当前页面发现十个以上重要的子页面时，认为该页面也是重要的，并将所有子页面标记为重要
            tool.save(url + '\n', 'a', name="important")
            url_dict[url] = 1
        else:
            url_dict[url] = 0
        level = url_dict[url]
        for link in links:
            url_dict[link] = level
        return links



    def getHost(self, url):
        """
        获取url中的域名
        @:param url
        """
        r = re.compile(r'(https?://)?[^/\s]*', re.S)
        g = r.match(url)
        host = ''.join(g.group())
        return host

    def judgePage(self, url):
        """
        判断url是否为html类型的
        @:param url
        """
        r = re.compile('[xs]?htm[l]?$')
        s = re.findall(r, url)
        return len(s) == 1





class MyQueue:
    """
    一个模拟队列的数据结构，这里做了个优化：
    通过使用两个unVisited列表（first，second）实现多级队列，从而使感兴趣的内容能够尽快被访问到，而不是被其他无用的内容抢先
    """

    def __init__(self):
        self.visited = []
        self.unVisitedFirst = []  # 采用多级队列实现优先级分级
        self.unVisitedSecond = []

    def getVisitedUrls(self):
        return self.visited

    def getUnvisitedUrls(self):
        return self.unVisitedFirst.extend(self.unVisitedSecond)

    def addVisitedUrl(self, url):
        self.visited.append(url)

    def removeVisitedUrl(self, url):
        self.visited.remove(url)

    # 将最后一个元素（即队列头）移出列表
    def unVisitedDequeue(self):
        try:
            if len(self.unVisitedFirst) > 0:  # 只有当一级队列为空时，才返回二级队列的内容
                return self.unVisitedFirst.pop()
            else:
                return self.unVisitedSecond.pop()
        except:
            return None

    # 将新加入的url插入到列表头（即对列尾），先进先出
    def addUnvisitedUrl(self, url, level):
        if url != '':
            if level == 1:
                self.unVisitedFirst.insert(0, url)
            else:
                self.unVisitedSecond.insert(0, url)

    def getVisitedNums(self):
        return len(self.visited)

    def getunVisitedNums(self):
        return len(self.unVisitedFirst) + len(self.unVisitedSecond)

    def isUnvisitedEmpty(self):
        return len(self.unVisitedFirst) == 0 and len(self.unVisitedSecond) == 0


class Tool:
    """
    类如其名，一个封装了各种操作的工具类
    包括：	1.html页面标签过滤
    		2.解压gzip压缩的页面
    		3.保存文件到磁盘中
    		4.删除特定目录下的文件
    		5.通过url抓取页面，经过各种处理后，返回字符串
    """

    path = os.getcwd() + os.sep + 'news' + os.sep
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Referer': 'http://www.google.com',
    }

    def replaceCharEntity(self, htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }
        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()
            key = sz.group('name')
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # 以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    def filter_tags(self, htmlstr):
        re_nav = re.compile('<nav.+</nav>')
        re_cdata = re.compile('//<!\[CDATA\[.*//\]\]>', re.DOTALL)
        re_script = re.compile(
            '<\s*script[^>]*>.*?<\s*/\s*script\s*>', re.DOTALL | re.I)
        re_style = re.compile(
            '<\s*style[^>]*>.*?<\s*/\s*style\s*>', re.DOTALL | re.I)
        re_textarea = re.compile(
            '<\s*textarea[^>]*>.*?<\s*/\s*textarea\s*>', re.DOTALL | re.I)
        re_br = re.compile('<br\s*?/?>')
        re_h = re.compile('</?\w+.*?>', re.DOTALL)
        re_comment = re.compile('<!--.*?-->', re.DOTALL)
        re_space = re.compile(' +')
        s = re_cdata.sub('', htmlstr)
        s = re_nav.sub('', s)
        s = re_script.sub('', s)
        s = re_style.sub('', s)
        s = re_textarea.sub('', s)
        s = re_br.sub('', s)
        s = re_h.sub('', s)
        s = re_comment.sub('', s)
        s = re.sub('\\t', '', s)
        # s = re.sub(' ', '', s)
        s = re_space.sub(' ', s)
        s = self.replaceCharEntity(s)
        return s

    def replace(self, content):
        r = re.compile(r'<script.*?</script>', re.I | re.M | re.S)  # 删除JavaScript
        s = r.sub('', content)
        r = re.compile(r'<style.*?</style>', re.I | re.M | re.S)  # 删除css
        s = r.sub('', s)
        r = re.compile(r'<!--.*?-->', re.I | re.M | re.S)  # 删除注释
        s = r.sub('', s)
        r = re.compile(r'<meta.*?>', re.I | re.M | re.S)  # 删除meta
        s = r.sub('', s)
        r = re.compile(r'<ins.*?</ins>', re.I | re.M | re.S)  # 删除ins
        s = r.sub('', s)
        r = re.compile(r'<[^>]+>', re.M | re.S)
        s = r.sub('', s).strip()  # 删除HTML标签
        r = re.compile(r'^\s+$', re.M | re.S)  # 删除空白行
        s = r.sub('', s)
        r = re.compile(r'\n+', re.M | re.S)  # 合并空行为一行
        s = r.sub('\n', s)
        r = re.compile('\s+', re.I | re.M | re.S)
        s = r.sub('\n', s)
        s = self.filter_tags(s)
        return self.replaceCharEntity(s)

    # 解压gzip压缩的网页
    def gzdecode(self, data):
        charset = chardet.detect(data)['encoding']
        if charset == None:
            charset = 'utf-8'
        if charset.lower() == 'gb2312':
            charset = 'gb18030'
        try:
            html = gzip.decompress(data).decode(charset)
        except OSError:
            html = data.decode(charset)
        return html

    def save(self, data, option='w', name='out'):
        path = self.path
        if os.path.exists(path) == False:
            os.makedirs(path)
        f = open(path + name + '.txt', option, encoding='utf-8')
        f.write(data)
        f.close()

    def remove(self, name):
        path = self.path + name + '.txt'
        if os.path.exists(path):
            print('remove...')
            os.remove(path)
        else:
            return

    def fetchPage(self, url):
        page = ''
        for i in range(3):
            try:
                socket.setdefaulttimeout(5)
                req = request.Request(url, headers=self.headers)
                page = request.urlopen(req).read()
                page = self.gzdecode(page)
                # print('success')
                return page
            except request.HTTPError as e:
                print(e.reason)
                return ''
            except request.URLError as e:
                print(e.reason)
                return ''
            except socket.timeout as e:
                if i < 2:
                    continue
                else:
                    print('timeout')
                    return ''
            except:
                print('other error')
                return ''


if __name__ == '__main__':
    tool = Tool()
    spider = MySpider(urls)
    spider.crawl(10)
