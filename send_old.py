# -*- coding: utf-8 -*-
"""方法:

如果random 取电影id, 先判断sended的状态, 如果为0, 说明之前还没发过,
然后查询是否还有相同电影id的条目, 如果有, 则取出其下载地址, 使用sina
短网址api 压缩多个下载地址, 发布微博, 然后使已发送成功的条目的sended字段置1.

"""


activate_this = 'venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from strs2weibo import  send_weibo


def main():
    topic = u'电影传送门'
    query = """SELECT douban_title, download_url, douban_url, lpic_url, douban_id FROM
            movie WHERE douban_id in (SELECT douban_id FROM movie ORDER BY
            random() LIMIT 1) and sended=0"""
    update = "UPDATE movie SET sended=1 WHERE douban_id=?"
    send_weibo(topic, query, update) 

if __name__ == '__main__':
    main()
