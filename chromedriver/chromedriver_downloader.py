import os.path
import sys
import threading
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class GradleDistributions:

    def __init__(self):
        self.distributions = []
        self.host_url = 'https://googlechromelabs.github.io/chrome-for-testing/#stable'
        self.gradle_dir = '/Volumes/WDDATA/application/chromedriver'
        self.download_index = 0
        self.lock = threading.Lock()

    def start(self):
        self._fetch_distributions()
        self.download_index = 0
        print(f'distributions count: {len(self.distributions)}')
        for distribution in self.distributions:
            print(distribution)
        threads = []
        for i in range(8):
            t = threading.Thread(target=self._download_distributions, args=(i,), daemon=True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

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
        chrome_options.add_argument('--headless')  # 无界面模式
        service = Service('/Users/zhouzhenliang/bin/chromedriver-mac-x64/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(self.host_url)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')
        stable_section = soup.find('section', id='stable')
        tbody = stable_section.find('tbody')
        trs = tbody.find_all('tr')
        for tr in trs:
            codes = tr.find_all('code')
            binary, platform, url, status = map(lambda x: x.text.strip(), codes)
            if binary == 'chromedriver':
                self.distributions.append((platform, url))

    def _download_distribution(self, distribution, index, tid):
        platform, url = distribution
        dir_path, name = os.path.split(url)
        dst_path = os.path.join(self.gradle_dir, platform, name)
        if os.path.exists(dst_path):
            self._log(f'{tid} {index}, file exist, path: {dst_path}')
            return

        self._log(f'{tid} {index}, start download, path: {dst_path}')
        start_time = time.time()
        try:
            response = requests.get(url, stream=True)  # 开启流式下载
            response.raise_for_status()  # 检查请求是否成功
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
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
