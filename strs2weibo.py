#!/usr/bin/env python
# -*- coding: utf-8 -*-

activate_this = 'bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from datetime import datetime
from hashlib import md5
import re
from urllib import urlretrieve
from urlparse import urljoin
from bs4 import BeautifulSoup
import requests
from weibo import APIClient
from config import APP_KEY, APP_SECRET, ACCESS_TOKEN, EXPIRES_IN,\
    CALLBACK_URL, ROOT, API_KEY


__version__ = '0.1.0'
__author__ = 'holys <chendahui007@gmail.com>'


def parse_sourcelist(url):
    """Parse sourcelist to get filedetail url"""

    thisid_re = re.compile(r"VodAdmin\/(.+?)\'")
    response = session.get(url)
    response.encoding = 'utf-8'
    return  list(set(thisid_re.findall(response.text)))


def parse_detail(url):
   """Parse detail information"""

   res = requests.get(url)
   res.encoding = 'utf-8'
   content = res.text
   soup = BeautifulSoup(content)
   title_re = re.compile(ur"节目名称：\s+(.+)?</td>", re.M)
   date_re = re.compile(ur"创建日期.\s(.+)?<")

   title = re.search(title_re, content).group(1)
   upload_date = re.search(date_re, content)

   #import pdb; pdb.set_trace()
   download_url = soup.find_all('a')[2].get('href').encode('utf8')
   poster_url = soup.find_all('img')[0].get('src')
   return (title, upload_date, download_url, poster_url) 

   
def parse_douban(title):
    """Parse douban movie api result"""

    result = requests.get('https://api.douban.com/v2/movie/search?q=%s&apikey=%s' %\
        (title, API_KEY)).json()
    if result.get('total') == 0:
        return 
    else:
        title = result.get('subjects',{})[0].get('title')
        alt = result.get('subjects', {})[0].get('alt')
        lpic = result.get('subjects',\
                [''])[0].get('images').get('large').replace('\\', '')
        return (title, alt, lpic)


def count_page(url):
    """ Count how many pages of certain url"""

    page_re = re.compile(ur"共<.+?>(\d{1,5})<")
    response = requests.get(url)
    response.encoding = 'utf-8'
    return  int(re.search(page_re,response.text).group(1))
    

def retrieve_image(url):
    """Retrieve an image from Internet and return image local path"""

    return open(list(urlretrieve(url))[0], 'rb')




def check_update(date):
    """ Check if there are new contents """
    
    format_date = datetime.strptime(date, '%Y-%m-%d')
    return  format_date == datetime.now()


def check_sended(msg):
    """Check if sended before"""
    
    sended = False
    with open(datetime.now().strftime('%Y-%m-%d'), 'a+') as datefile:
        if md5(msg).hexdigest() in datefile.read():
            print 'Sended before'
            sended = True
        else:
            datefile.write(md5(msg).hexdigest())
    return sended
    

def weibo_upload(status, pic):
    """Tweet with image
    
    +-----------------------------------------------------------+
    | +--------------+----------+-----------+--------+--------+ |
    | | #电影传送门# | 电影名称 |下载地址URL| 详情URL| 豆瓣URL| |
    | +--------------+----------+-----------+--------+--------+ |
    |                    电影海报(图片)                         |
    +-----------------------------------------------------------+
    """

    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET,\
        redirect_uri=CALLBACK_URL)
    client.set_access_token(ACCESS_TOKEN, EXPIRES_IN)
    return client.statuses.upload.post(status=status, pic=pic)


def construct_status(title, download_url, detail_url, alt):
    """Construct weibo message """

    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET,\
        redirect_uri=CALLBACK_URL)
    client.set_access_token(ACCESS_TOKEN, EXPIRES_IN)
    download_url =\
        client.short_url.shorten.get(url_long=download_url).get('urls')[0].get('url_short')
    status = u"#电影传送门#《%s》 下载:%s 详情:%s 豆瓣电影:%s" %(title,\
            download_url, detail_url, alt)
    return status


if __name__ == '__main__':
    activate_this = 'bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))
    session = requests.Session()
    session.get(ROOT)
    url = 'http://strs.gdufs.edu.cn/web/VOD/vod_sourcelist.asp?Groupid=1&page=1'
    for item in parse_sourcelist(url):
        detail_url = urljoin(ROOT, item)
        title = parse_detail(detail_url)[0] 
        download_url = parse_detail(detail_url)[2]
        alt = parse_douban(title)[1]
        pic = retrieve_image(parse_douban(title)[2])
        status = construct_status(title, download_url, detail_url, alt)
        print status
#        weibo_upload(status, pic)

