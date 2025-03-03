import os.path
import sys
import threading
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from mp3.mysql_connection import open_mysql


class Mp3Distributions:

    def __init__(self):
        self.driver = None
        self.distributions = []
        self.gradle_dir = '/Volumes/WDDATA4T/audio'
        self.download_index = 0
        self.lock = threading.Lock()

    def start(self):
        # chromedriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无界面模式
        service = Service('/Users/zhouzhenliang/bin/chromedriver-mac-x64/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        for page in range(1, 2167):
            self._fetch_distributions(page)
            for dist in self.distributions:
                sql = f'REPLACE INTO audio_kumeiwp(detail_url,name,size,upload_user,upload_time,page_url) VALUES(%s,%s,%s,%s,%s,%s)'
                values = (
                    dist['detail_url'],
                    dist['name'],
                    dist['size'],
                    dist['upload_user'],
                    dist['upload_time'],
                    dist['page_url'])
                with open_mysql() as cursor:
                    cursor.execute(sql, values)

        self.download_index = 0
        print(f'distributions count: {len(self.distributions)}')
        # threads = []
        # for i in range(8):
        #     t = threading.Thread(target=self._download_distributions, args=(i,), daemon=True)
        #     threads.append(t)
        #     t.start()
        # for t in threads:
        #     t.join()

        self.driver.quit()

    def _download_distributions(self, i):
        while True:
            with self.lock:
                index = self.download_index
                self.download_index += 1
            if index >= len(self.distributions):
                break
            self._download_distribution(self.distributions[index], index, i)

    def _fetch_distributions(self, page):
        self.distributions.clear()

        page_url = f'https://www.kumeiwp.com/cate/1-{page}.html'
        self.driver.get(page_url)
        table = self.driver.find_element(By.ID, 'f_tab')
        if not table:
            return
        trs = table.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            tr_class = tr.get_attribute('class')
            if tr_class != 'color1' and tr_class != 'color4':
                continue

            row_href = None
            row_name = None
            row_size = None
            row_upload_time = None
            row_upload_user = None
            tds = tr.find_elements(By.TAG_NAME, 'td')
            if tds and len(tds) == 4:
                td1 = tds[0]
                link1 = td1.find_element(By.TAG_NAME, 'a')
                if link1:
                    row_href = link1.get_attribute('href')
                    row_name = link1.text.strip()
                td2 = tds[1]
                link2 = td2.find_element(By.TAG_NAME, 'a')
                if link2:
                    row_upload_user = link2.text.strip()
                td3 = tds[2]
                row_size = td3.text.strip()
                td4 = tds[3]
                row_upload_time = td4.text.strip()
            if row_href and row_name and row_size and row_upload_time:
                item = {
                    'detail_url': row_href,
                    'name': row_name,
                    'size': row_size,
                    'upload_user': row_upload_user,
                    'upload_time': row_upload_time,
                    'page_url': page_url,
                }
                self.distributions.append(item)
                print(f'item = {item}')

    def _download_distribution(self, url: str, index, tid):
        dir_path, name = os.path.split(url)
        dst_path = os.path.join(self.gradle_dir, name)
        if os.path.exists(dst_path):
            self._log(f'{tid} {index}, file exist, path: {dst_path}')
            return

        self._log(f'{tid} {index}, start download, path: {dst_path}')
        start_time = time.time()
        try:
            response = requests.get(url, stream=True)  # 开启流式下载
            response.raise_for_status()  # 检查请求是否成功
            with open(dst_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):  # 分块写入
                    file.write(chunk)
            self._log(
                f'{tid} {index}, download success, path: {dst_path}, duration: {round(time.time() - start_time, 2)}s')
        except requests.RequestException as e:
            if os.path.exists(dst_path):
                os.remove(dst_path)
            self._log(
                f'{tid} {index}, download fail, , path: {dst_path}, duration: {round(time.time() - start_time, 2)}s, e: {e}',
                file=sys.stderr)

    def _log(self, message, file=None):
        with self.lock:
            print(message, file=file)


if __name__ == '__main__':
    impl = Mp3Distributions()
    impl.start()
