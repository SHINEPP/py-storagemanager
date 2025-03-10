import os.path
import sys
import time

import requests

from mp3.mysql_connection import open_mysql


class AudioDownloader:

    def __init__(self):
        self.repository_dir = '/Volumes/US100/audio/kumeiwp/repository'
        pass

    def start(self):
        sql = 'SELECT name, download_url, local_path FROM audio_kumeiwp_detail_view WHERE download_times <= %s'
        with open_mysql() as cursor:
            cursor.execute(sql, 0)
            for row in cursor:
                name = row[0]
                download_url = row[1]
                local_path = row[2]
                self._process_row(name, download_url, local_path)

    def _process_row(self, name, download_url, local_path):
        path = self.repository_dir + local_path
        tmp_path = path + '.tmp_download'
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        if os.path.exists(path):
            print(f'file exist, {name}, path: {local_path}', file=sys.stderr)
            return

        msg = f'{download_url}'
        print(f'start download, {name}, {msg}', end='')
        start_time = time.time()
        try:
            response = requests.get(download_url, stream=True)  # 开启流式下载
            content_type = response.headers.get('Content-Type', '')
            content_length = int(response.headers.get('Content-Length', '0'))
            if content_type == 'application/octet-stream':
                response.raise_for_status()  # 检查请求是否成功
                os.makedirs(os.path.dirname(path), exist_ok=True)
                total_text = None
                if content_length > 0:
                    total_text = f'{round(content_length / 1024 / 1024, 3)}MB'
                with open(tmp_path, 'wb') as file:
                    size = 0
                    for chunk in response.iter_content(chunk_size=8192):  # 分块写入
                        file.write(chunk)
                        size += len(chunk)
                        size_text = f'{round(size / 1024 / 1024, 3)}MB'
                        if total_text:
                            print(f'\rdownloading, {name}, {msg}, {size_text}/{total_text}', end='')
                        else:
                            print(f'\rdownloading, {name}, {msg}, {size_text}', end='')
                os.rename(tmp_path, path)
                dur_text = round(time.time() - start_time, 2)
                print(f'\rdownload success, {name}, {msg}, size: {total_text} duration: {dur_text}s')
            else:
                dur_text = round(time.time() - start_time, 2)
                print(f'\rdownload fail, {name}, {msg}, {response.text}, duration: {dur_text}s', file=sys.stderr)
        except Exception as e:
            if os.path.exists(path):
                os.remove(path)
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            dur_text = round(time.time() - start_time, 2)
            print(f'\rdownload fail, {name}, {msg}, duration: {dur_text}s, e: {e}', file=sys.stderr)

        sql = 'UPDATE audio_kumeiwp_detail SET download_times = download_times + 1 WHERE download_url = %s'
        with open_mysql() as cursor:
            cursor.execute(sql, download_url)


if __name__ == '__main__':
    impl = AudioDownloader()
    impl.start()
