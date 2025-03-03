import os.path
import sys
import time

import requests

from mp3.mysql_connection import open_mysql


class Mp3Syncer:

    def __init__(self):
        self.repository_dir = '/Volumes/WDDATA4T/audio/kumeiwp/repository'
        pass

    def start(self):
        sql = 'SELECT download_url, local_path FROM audio_kumeiwp_detail'
        with open_mysql() as cursor:
            cursor.execute(sql)
            for row in cursor:
                download_url = row[0]
                local_path = row[1]
                path = self.repository_dir + local_path
                if os.path.exists(path):
                    print(f'file exist, path: {local_path}', file=sys.stderr)
                    continue

                msg = f'{download_url} -> {local_path}'
                print(f'start download, {msg}', end='')
                start_time = time.time()
                try:
                    response = requests.get(download_url, stream=True)  # 开启流式下载
                    response.raise_for_status()  # 检查请求是否成功
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, 'wb') as file:
                        size = 0
                        for chunk in response.iter_content(chunk_size=8192):  # 分块写入
                            file.write(chunk)
                            size += len(chunk)
                            print(f'\rdownload progress, {msg}, {round(size / 1024 / 1024, 3)}MB', end='')
                    dur_text = round(time.time() - start_time, 2)
                    print(f'\rdownload success, {msg}, duration: {dur_text}s')
                except requests.RequestException as e:
                    if os.path.exists(path):
                        os.remove(path)
                    dur_text = round(time.time() - start_time, 2)
                    print(f'\rdownload fail, {msg}, duration: {dur_text}s, e: {e}', file=sys.stderr)


if __name__ == '__main__':
    impl = Mp3Syncer()
    impl.start()
