import os.path

import requests

x_apikey = '3ff336ede3210e7cd3c29377d0fafd07fb8ba2e999934bde845eca286bedb39a'


def upload_apk(apk: str):
    """
    result: https://www.virustotal.com/gui/file-analysis/[id]
    """
    url = 'https://www.virustotal.com/api/v3/files'
    files = {'file': (os.path.splitext(apk)[-1], open(apk, 'rb'), 'application/vnd.android.package-archive')}
    headers = {
        'accept': 'application/json',
        'x-apikey': x_apikey
    }
    response = requests.post(url, files=files, headers=headers)
    print(response.text)


def get_report(file_id: str):
    """
    :param file_id: SHA-256, SHA-1 or MD5 identifying the file
    """
    url = f'https://www.virustotal.com/api/v3/files/{file_id}'
    headers = {
        'accept': 'application/json',
        'x-apikey': x_apikey
    }

    response = requests.get(url, headers=headers)
    print(response.text)


if __name__ == '__main__':
    path = '/Users/zhouzhenliang/Desktop/app-release.apk'
    # upload_apk(path)
    get_report('1d1ad281426db09c069a46e1cc3c843fd17db0dee35a367e5e030a791ef8e71b')
