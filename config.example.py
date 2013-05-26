from urlparse import urljoin

APP_KEY = 'YOUR APP_KEY'
APP_SECRET = 'YOUR APP_SECRET'
ACCESS_TOKEN = 'YOUR ACCESS_TOKEN'
EXPIRES_IN = 'YOUR_EXPIRES_IN'
CALLBACK_URL = 'http://example.com:8080'

# douban 
API_KEY = 'YOUR API_KEY'


ROOT = 'http://strs.gdufs.edu.cn/web/'
BASIC_URL = 'VOD/vod_sourcelist.asp?Groupid=%d&FirstTypeID=%d'

INDEX = {
        'xydt': {
            'group_id': 3,
            'firsttype_id': {
                'sstj': 3391,
                'xywh': 3546,
                'gwmsgkk': 2874,
                'mxmsgkk': 2142,
                'mtgw': 1228,
                'jslt': 818,
                'bkyd': 3109,
                'ycdv': 2805,
                'xshd': 1788,
                'jzypx': 824
                }
            },
        'dsjj': {
            'group_id': 2,
            'firsttype_id': {
                'bbc': 30,
                'cnn': 3133,
                'cctv_news': 20,
                'newsasia': 2132,
                'mzt': 44,
                'gjt': 27,
                'gzyyt': 35,
                'hall': 52,
                'gjdl': 104,
                'tspd': 28,
                'French': 58,
                'German': 59,
                'Spanish': 60,
                'Indonesian': 55,
                'Japanese': 56,
                'Italian': 50,
                'Russian': 51,
                'R1TV': 1212,
                'JPBS': 759,
                'Portuguese': 229,
                'Vietnamese': 53,
                'ysgj': 15,
                'wywh': 3412,
                'agys': 12,
                'yskj': 21,
                'Arabic': 29
                }
            },
        'dyjx': {
            'group_id': 1,
            'firsttype_id': {
                'western': 879,
                'inland': 875,
                'HKTW': 877,
                'Asia': 881,
                'Classic': 899,
                'anime': 893
                }
            },
        'szjy': {
            'group_id': 4,
            'firsttype_id': {
                'dyxx': 3207,
                'qdhd': 3416,
                'ssjd': 3406,
                'aqjy': 836
                }
            },
        'jxkj': {
                'group_id': 5,
                'firsttype_id': {
                    'jxkj': 1100,
                    'xyyytl': 4188
                    }
                }
}


def enumerate_index(index=INDEX):
    all_url = []
    for values in index.itervalues():
        for value in values.get('firsttype_id').itervalues():
            all_url.append(urljoin(ROOT, BASIC_URL) % (values.get('group_id'),
                value))
    return all_url


