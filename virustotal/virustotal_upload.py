import json
import os.path

import requests

x_apikey = '3ff336ede3210e7cd3c29377d0fafd07fb8ba2e999934bde845eca286bedb39a'


def get_large_file_url():
    url = 'https://www.virustotal.com/api/v3/files/upload_url'
    headers = {
        'accept': 'application/json',
        'x-apikey': x_apikey
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    result = json.loads(response.text)
    return result['data']


def upload_file(file: str):
    """
    result: https://www.virustotal.com/gui/file-analysis/[id]
    """
    file_size = os.path.getsize(file)
    if file_size > 32 * 1024 * 1024:
        url = get_large_file_url()
    else:
        url = 'https://www.virustotal.com/api/v3/files'

    files = {'file': (os.path.split(file)[-1], open(file, 'rb'), 'application/vnd.android.package-archive')}
    headers = {
        'accept': 'application/json',
        'x-apikey': x_apikey
    }
    response = requests.post(url, files=files, headers=headers)
    print(response.text)

    result = json.loads(response.text)
    print(f'https://www.virustotal.com/gui/file-analysis/{result["data"]["id"]}')


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


def _main():
    path = '/Users/zhouzhenliang/Downloads/app-release_0226110827.apk'
    upload_file(path)


if __name__ == '__main__':
    _main()
