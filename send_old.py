# -*- coding: utf-8 -*-
"""方法:

如果random 取电影id, 先判断sended的状态, 如果为0, 说明之前还没发过,
然后查询是否还有相同电影id的条目, 如果有, 则取出其下载地址, 使用sina
短网址api 压缩多个下载地址, 发布微博, 然后使已发送成功的条目的sended字段置1.

"""


activate_this = 'venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from sqlite3 import dbapi2 as sqlite3
from strs2weibo import retrieve_image, construct_status, weibo_upload


_db = 'data/production.db'


def _fetch_data():
    """Fetch data from db for preparing tweeting message """

    with sqlite3.connect(_db) as conn:
        cursor = conn.cursor()
        query = """SELECT douban_title, douban_url, lpic_url, douban_id FROM
                movie WHERE douban_id in (SELECT douban_id FROM movie ORDER BY
                random() LIMIT 1) and sended=0"""
        cursor.execute(query)
        rows = cursor.fetchall()
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


def main():
    topic = u'电影传送门'
    douban_title, download_url, douban_url, lpic_url, douban_id = _fetch_data()
    lpic = retrieve_image(lpic_url)
    status = construct_status(topic, douban_title, douban_url, *download_url)
    response =  weibo_upload(status=status, pic=lpic)
    if response.get('created_at'):
        with sqlite3.connect(_db) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE movie SET sended=1 WHERE douban_id=?",\
                    (douban_id,))
            print "\nWeibo sented successfully !\n","douban_id:", douban_id
    elif response.get('error_code'):
        print response.get('error_code'), response.get('error')
    else:
        print "Unknown Error!"


if __name__ == '__main__':
    main()
