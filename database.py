#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from sqlite3 import dbapi2 as sqlite3
from config import API_KEY
from strs2weibo import parse_douban


_database = 'data/movie.db'
_schema = 'schema.sql'
_detail = 'detail.txt'

    
def create_db():
    with sqlite3.connect(_database) as conn:
        print 'Creating schema'
        with open(_schema, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
        conn.text_factory = str
        cursor = conn.cursor()
        f = open(_detail)
        for line in f.readlines()[30:40]:
            (title, download_url, movie_url) = line.split('|')
            try:
                (douban_title, douban_url, lpic_url) = parse_douban(title,
                        api_key=API_KEY)
                print title,'<><><>', douban_title
                data = (title, download_url, movie_url, douban_url,\
                        douban_title, lpic_url)
                cursor.execute("""
                insert into movie (title, download_url, movie_url, douban_url,
                douban_title, lpic_url) values(?,?,?,?,?,?)""", data)
                time.sleep(1)
            except TypeError:
                print "%s not found in Douban" % title
                with open('error.txt', 'a') as ff:
                    ff.write(title.encode('utf8'))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_db()


