import os.path
import sys
import threading
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from common import calculate_sha256


class GradleDistributions:

    def __init__(self):
        self.distributions = []
        self.host_url = 'https://jdk.java.net/archive/'
        self.gradle_dir = '/Volumes/WDDATA/openjdk/archive'
        self.download_index = 0
        self.lock = threading.Lock()

    def start(self):
        self._check_distributions()
        # self._fetch_distributions()
        # self.download_index = 0
        # print(f'distributions count: {len(self.distributions)}')
        # threads = []
        # for i in range(8):
        #     t = threading.Thread(target=self._download_distributions, args=(i,), daemon=True)
        #     threads.append(t)
        #     t.start()
        # for t in threads:
        #     t.join()

    def _check_distributions(self):
        paths = []
        for root, dirs, files in os.walk(self.gradle_dir):
            for file in files:
                if file.endswith('.sha256'):
                    continue
                path = os.path.join(root, file)
                paths.append(path)

        print(f'count: {len(paths)}')
        index = -1
        for path in paths:
            index += 1
            print(f'check file, index = {index}, path: {path}')
            sha256 = path + '.sha256'
            if not os.path.exists(sha256):
                os.remove(path)
                print(f'rm file, no sha256 file, path: {path}')
                continue
            with open(sha256, 'r') as f:
                content = f.read().strip()
                if '=' in content:
                    _, content = content.split('=')[-1].strip()
            value = calculate_sha256(path)
            print(f'sha256, file: {value}, sha256: {content}')
            if not value == content:
                os.remove(path)
                os.remove(sha256)
                print(f'rm file, sha256 no equal: {value} != {content}, path: {path}', file=sys.stderr)

    def _download_distributions(self, i):
        while True:
            with self.lock:
                index = self.download_index
                self.download_index += 1
            if index >= len(self.distributions):
                break
            self._download_distribution(self.distributions[index], index, i)

    def _fetch_distributions(self):
        self.distributions.clear()

        # chromedriver
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 无界面模式
        service = Service('/Users/zhouzhenliang/bin/chromedriver-mac-x64/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(self.host_url)
        html = driver.page_source
        with open('archive.html', 'w') as file:
            file.write(html)
        driver.quit()
        soup = BeautifulSoup(html, 'html.parser')
        download_table = soup.find(attrs={'summary': 'Downloads'})
        tds = download_table.find_all('td')
        for td in tds:
            links = td.find_all('a')
            for link in links:
                href = link['href']
                self.distributions.append(href)

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
    impl = GradleDistributions()
    impl.start()
