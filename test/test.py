#!usr/bin/env python
# -*- coding: utf-8 -*-

activate_this = './bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
from config import APP_KEY, APP_SECRET, ACCESS_TOKEN, EXPIRES_IN,\
CALLBACK_URL, ROOT
from weibo import APIClient
import requests



def weibo_upload(status, pic):
    """Tweet with image
    
    +-----------------------------------------------------------+
    | +--------------+----------+-----------+--------+--------+ |
    | | #电影传送门# | 电影名称 |下载地址URL| 详情URL| 豆瓣URL| |
    | +--------------+----------+----------+------------------+ |
    |                    电影海报(图片)                         |
    +-----------------------------------------------------------+
    """

    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET,\
        redirect_uri=CALLBACK_URL)
    client.set_access_token(ACCESS_TOKEN, EXPIRES_IN)
    return client.statuses.upload.post(status=status, pic=pic)
     

if __name__ == '__main__':
    url = 'http://strs.gdufs.edu.cn/web/VOD/vod_sourcelist.asp?Groupid=1'  
    s = requests.Session()
    s.get(ROOT)
    import pdb; pdb.set_trace()
    print sys.path
    




