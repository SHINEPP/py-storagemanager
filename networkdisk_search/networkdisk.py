import json

import requests

DISK_URL = 'https://hunhepan.com/open/search/disk'

TIME_WEEK = 'week'
TIME_MONTH = 'month'
TIME_THREE_MONTH = 'three_month'
TIME_YEAR = 'year'

TYPE_BDY = 'BDY'
TYPE_ALY = 'ALY'
TYPE_QUARK = 'QUARK'
TYPE_XUNLEI = 'XUNLEI'


def search(word):
    data = {
        'q': word,
        'page': 1,
        'size': 10,
        'time': TIME_MONTH,
        'type': TYPE_QUARK,
        'exact': True
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(DISK_URL, headers=headers, json=data)
    content = response.content
    print(f'content = {content}')


if __name__ == '__main__':
    search('功夫熊猫')
