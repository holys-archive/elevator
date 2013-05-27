#!/usr/bin/env python

from sqlite3 import dbapi2 as sqlite3
import os
from config import API_KEY
from strs2weibo import parse_douban


_database = 'data/movie.db'
_schema = 'schema.sql'
_detail = 'detail.txt'



def get_douban_info():
    with open(_detail, 'r') as f:
        for line in f.readlines():
            (title, download_url, movie_url) = line.split('|')
            try:
                (douban_title, douban_url, lpic_url) = parse_douban(title,
                        api_key=API_KEY)
                print title,'<><><>', douban_title
            except TypeError:
                print "%s not found in Douban" % title
                with open('error.txt', 'a') as ff:
                    ff.write(title.encode('utf8'))
    return (title, download_url, movie_url, douban_url, douban_title, lpic_url)



def create_db(data):
    with sqlite3.connect(_database) as conn:
        if db_is_new:
            print 'Creating schema'
            with open(_schema, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)
            cursor = conn.cursor()
    
            print 'Inserting movie data'
            cursor.execute("""
            insert into movie (title, download_url, movie_url, douban_url,
            douban_title, lpic_url, ) values(?)""", data)

            conn.commit()
            conn.close()
    
        else:
            print 'Database exists'

if __name__ == '__main__':
    import pdb; pdb.set_trace()
    db_is_new = not os.path.exists(_database)
    get_douban_info()
    #create_db(data)  
