import os.path
import sys
import threading
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class GradleDistributions:

    def __init__(self):
        self.distributions = []
        self.host_url = 'https://www.kumeiwp.com/cate/1.html'
        self.gradle_dir = '/Volumes/WDDATA4T/audio'
        self.download_index = 0
        self.lock = threading.Lock()

    def start(self):
        self._fetch_distributions()
        self.download_index = 0
        print(f'distributions count: {len(self.distributions)}')
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
        contents = driver.find_element(By.ID, 'f_tab')
        if not contents:
            return
        items = contents.find_elements(By.TAG_NAME, 'tr')
        if not items:
            return
        for item in items:
            clazz = item.get_attribute('class')
            if clazz != 'color1' and clazz != 'color4':
                continue
            tds = item.find_elements(By.TAG_NAME, 'td')
            if not tds:
                continue
            for td in tds:
                clazz = td.get_attribute('class')
                if clazz != 'f14':
                    continue
                link = td.find_element(By.TAG_NAME, 'a')
                if not link:
                    continue
                href = link.get_attribute('href')
                if not href:
                    continue
                try:
                    driver.get(href)
                except Exception as e:
                    print(f'error, e = {e}')
                    continue
                content = driver.find_element(By.CLASS_NAME, 'layui-col-md12')
                if content:
                    link = content.find_element(By.TAG_NAME, 'a')
                    if link:
                        href = link.get_attribute('href')
                        self.distributions.append(href)
                        print(href)

        driver.quit()

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
