#!/usr/bin/env python
# -*- coding: utf-8 -*-

activate_this = 'venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from datetime import datetime
from hashlib import md5
from sqlite3 import dbapi2 as sqlite3

import requests

from config import ROOT, DATABASE, API_KEY
from strs2weibo import parse_detail, parse_sourcelist, parse_douban, send_weibo


def _save_data(url, session, db):
    """Store data into movie_new for tweeting message later"""

    with sqlite3.connect(db) as conn:
        conn.text_factory = str
        cursor = conn.cursor()
        insert = """INSERT INTO movie_new (title, download_url, movie_url,
        douban_url, douban_title, douban_id, lpic_url, download_url_md5, upload_date) VALUES
        (?,?,?,?,?,?,?,?,?)"""
        query = """SELECT * from movie_new WHERE download_url_md5=?"""

        for item in parse_sourcelist(session=session, url=url):
            movie_url = item
            title, upload_date, download_url = parse_detail(item)
            download_url_md5 = md5(download_url).hexdigest()
            douban_title, douban_url, douban_id, lpic_url = \
                    parse_douban(title, api_key=API_KEY)
            data = (title, download_url, movie_url, douban_url, douban_title,\
                    douban_id, lpic_url, download_url_md5, upload_date)

            test = datetime.strptime('2013-05-28', '%Y-%m-%d').date() == \
                    datetime.strptime(upload_date, '%Y-%m-%d').date()
            #记得改回来啊
            #if check_update(upload_date) and not cursor.execute(query,
            #        (download_url_md5, )).fetchall():
            if test and not cursor.execute(query, (download_url_md5,)).fetchall():
                print "Can insert data", douban_title
                cursor.execute(insert, data)
                conn.commit()
            else:
                print "Can't insert data for duplicate content or no update"


def main():
    #1. save up-to-date data to database
    session = requests.Session()
    session.get(ROOT)
    url = 'http://strs.gdufs.edu.cn/web/VOD/vod_sourcelist.asp?Groupid=1'
    db = DATABASE
    _save_data(url, session, db)
    
    #2. send up-to-date content to sina weibo from database
    topic = u'最新上传'
    query = """select douban_title, download_url, douban_url, lpic_url, douban_id  from movie_new 
    where douban_id in (select douban_id from movie_new where upload_date in 
    (select strftime('%Y-%m-%d', 'now')) and sended=0 order by random() limit 1);"""
    update = "UPDATE movie_new SET sended=1 WHERE douban_id=?"
    # 一天最多也就可能有8条更新吧
    for i in xrange(8):
        send_weibo(topic, query, update)


if __name__ == '__main__':
    main()
    

