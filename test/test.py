#!usr/bin/env python
# -*- coding: utf-8 -*-

activate_this = 'venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import requests
from strs2weibo import parse_douban, parse_detail, parse_sourcelist,\
    contruct_status, retrieve_image, ROOT



if __name__ == '__main__':
    session = requests.Session()
    session.get(ROOT)
    url = 'http://strs.gdufs.edu.cn/web/VOD/vod_sourcelist.asp?Groupid=1&page=1'
    for detail_url in parse_sourcelist(session, url):
        
        title = parse_detail(detail_url)[0] 
        download_url = parse_detail(detail_url)[2]
        (douban_title, douban_url, douban_id, lpic_url ) = parse_douban(title)
        pic = retrieve_image(lpic_url)
        topic = u'电影传送门'
        status = construct_status(topic, douban_title, download_url, douban_url)
        print status
#        weibo_upload(status, pic)

    




