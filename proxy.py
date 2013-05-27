#-*- coding: utf-8 -*-
#import logging
#logging.basicConfig(level=logging.DEBUG)

import  random

proxy_list = []

HEADERS = [
    ('Accept', '*/*'),
    ('Accept-Charset', 'UTF-8,*;q=0.5'),
    ('Accept-Encoding', 'gzip,deflate,sdch'),
    ('Accept-Language', 'zh-CN,zh;q=0.8'),
    ('Cache-Control', 'no-cache'),
    ('Connection', 'keep-alive'),
    ('Host', 'api.douban.com'),
    ('Pragma', 'no-cache'),
    ('Referer:http', '//www.douban.com/group/dbapi/'),
]

USER_AGENT_LIST = (
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
    'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13',
    'Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.8 (KHTML, like Gecko) Chrome/23.0.1246.0 Safari/537.8',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
)

def read_proxy_list():
    for line in open('list.txt'):
        proxy_list.append(line.strip())


def random_proxy():
    return 'http://' + random.choice(proxy_list)


def random_headers():
    headers = HEADERS[:]
    headers.append(('User-Agent', random.choice(USER_AGENT_LIST)))
    return dict(headers)

if __name__ == '__main__':
    headers= random_headers()
    print headers

