#!/usr/bin/env python
# -*- coding: utf-8 -*-

activate_this = 'bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


import requests
from config import ROOT
from strs2weibo import parse_detail, parse_sourcelist

base_url = 'http://strs.gdufs.edu.cn/web/VOD/vod_sourcelist.asp?Groupid=1&page=%d'
session = requests.Session()
session.get(ROOT)
with open('detail.txt', 'w') as f:
    for page in xrange(1, 521):
        url = base_url % (page)
        for detail_url in parse_sourcelist(session, url):
           title = parse_detail(detail_url)[0].encode('utf8')
           download_url = parse_detail(detail_url)[2]
           print title, download_url, detail_url
           f.write('%s|%s|%s\n' % (title, download_url, detail_url.encode('utf8')))
    
