#!/usr/bin/env python
# -*- coding: utf-8 -*-

activate_this = 'venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from datetime import datetime
import re
from sqlite3 import dbapi2 as sqlite3
from urllib import urlretrieve
from urlparse import urljoin

from bs4 import BeautifulSoup
import requests
from weibo import APIClient

from config import APP_KEY, APP_SECRET, ACCESS_TOKEN, EXPIRES_IN,\
    CALLBACK_URL, ROOT, API_KEY, DATABASE
from proxy import random_headers, PROXY


__version__ = '0.1.0'
__author__ = 'holys <chendahui007@gmail.com>'


def parse_sourcelist(session, url):
    """Parse sourcelist to get filedetail url
    
    session = requests.Session()
    """

    thisid_re = re.compile(r"VodAdmin\/(.+?)\'")
    response = session.get(url)
    response.encoding = 'utf-8'
    detail_list = list(set(thisid_re.findall(response.text)))
    return [urljoin(ROOT, item) for item in detail_list]


def parse_detail(url):
   """Parse detail information"""

   res = requests.get(url)
   res.encoding = 'utf-8'
   content = res.text
   soup = BeautifulSoup(content)
   title_re = re.compile(ur"节目名称：\s+(.+)?</td>", re.M)
   date_re = re.compile(ur"创建日期.\s(.+)?<")

   title = re.search(title_re, content).group(1)
   upload_date = re.search(date_re, content).group(1).split(' ')[0].strip()
   # change date type `2013-5-29` to `20130529`
   upload_date = datetime.strftime(datetime.strptime(upload_date, '%Y-%m-%d'),
           '%Y-%m-%d')
   download_url = soup.find_all('a')[2].get('href').encode('utf8')
   return (title, upload_date, download_url) 

   
def parse_douban(title, api_key=API_KEY):
    """Parse douban movie api result"""

    headers = random_headers()
    proxies = PROXY
    url = 'https://api.douban.com/v2/movie/search?q=%s&apikey=%s' % (title,\
            api_key)
    result = requests.get(url, headers=headers, proxies=proxies).json()
    try:
        if result.get('msg'):
            print result.get('msg')
        if result.get('total') > 0:
            douban_title = result.get('subjects')[0].get('title')
            douban_url = result.get('subjects')[0].get('alt')
            douban_id = result.get('subjects')[0].get('id')
            lpic_url = result.get('subjects',\
                    )[0].get('images').get('large').replace('\\', '')
            return (douban_title, douban_url, douban_id, lpic_url)
        else:
            print "%s not found in douban" % title
    except IndexError:
        print "f*ck 豆瓣API, %s not found" % title 


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
    return  format_date.date() == datetime.now().date()


def fetch_data(query, db=DATABASE):
    """Fetch data from db for preparing tweeting message """

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            print "Can't query data from db"
            return False
        if len(rows) > 1:
            print '-' * 40
            douban_title = rows[0][0]
            douban_url = rows[0][2]
            lpic_url = rows[0][3]
            douban_id = rows[0][4]
            download_url = [row[1] for row in rows]
        else:
            douban_title, download_url, douban_url, lpic_url, douban_id = rows[0]
            download_url = [download_url]
    return douban_title, download_url, douban_url, lpic_url, douban_id


def weibo_upload(status, pic):
    """Tweet with image
    
    +-----------------------------------------------------------+
    | +--------------+----------+--------------------+--------+ |
    | | #电影传送门# | 电影名称 |下载地址URL1, URL2  | 豆瓣URL| |
    | +--------------+----------+--------------------+--------+ |
    |                    电影海报(图片)                         |
    +-----------------------------------------------------------+
    """

    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET,\
        redirect_uri=CALLBACK_URL)
    client.set_access_token(ACCESS_TOKEN, EXPIRES_IN)
    return client.statuses.upload.post(status=status, pic=pic)


def construct_status(topic, douban_title, douban_url, *download_url):
    """Construct weibo message """

    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET,\
        redirect_uri=CALLBACK_URL)
    client.set_access_token(ACCESS_TOKEN, EXPIRES_IN)
    download_url =\
        [client.short_url.shorten.get(url_long=url).get('urls')[0].get('url_short').encode('utf8')\
        for url in download_url]
    download_url = ' , '.join(download_url)
    status = u"#%s#《%s》 下载:%s 豆瓣电影:%s" %(topic, douban_title,\
            download_url, douban_url)
    return status


def send_weibo(topic, query, update):
    """Send weibo message and update database"""
    if not fetch_data(query):
        return 
    douban_title, download_url, douban_url, lpic_url, douban_id =\
       fetch_data(query)
    lpic = retrieve_image(lpic_url)
    status = construct_status(topic, douban_title, douban_url, *download_url)
    response =  weibo_upload(status=status, pic=lpic)
    db = DATABASE
    if response.get('created_at'):
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(update, (douban_id,))
            print "\nWeibo sented successfully !\n","douban_id:", douban_id
    elif response.get('error_code'):
        print response.get('error_code'), response.get('error')
    else:
        print "Unknown Error!"
