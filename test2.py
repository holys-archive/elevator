# -*- coding: utf-8 -*-
"""Send weibo manually"""


activate_this = 'venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from strs2weibo import  send_weibo


def main():
    topic = u'电影传送门'
    query = """SELECT douban_title, download_url, douban_url, lpic_url, douban_id FROM
            movie WHERE douban_id=3319755 and sended=1"""
    update = "UPDATE movie SET sended=1 WHERE douban_id=?"
    send_weibo(topic, query, update) 

if __name__ == '__main__':
    main()
