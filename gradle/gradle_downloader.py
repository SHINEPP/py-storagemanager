import hashlib
import os.path
import sys
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def fetch_gradle_distributions(url):
    """
    使用 Selenium 爬取动态网页
    """
    # 配置 Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无界面模式
    service = Service('/Users/zhouzhenliang/bin/chromedriver-mac-x64/chromedriver')

    # 启动 WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    # 等待加载完成并提取内容
    title = driver.title
    print(f'Page Title: {title}')

    contents = driver.find_element(By.ID, 'contents')
    if contents:
        items = contents.find_elements(By.CLASS_NAME, 'items')
        for item in items:
            links = item.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                if href:
                    print(href)
                    download_gradle_distribution_file(href)

    # 关闭浏览器
    driver.quit()


def download_gradle_distribution_file(url: str):
    gradle_dir = '/Volumes/WDDATA/gradle/distributions'
    dir_path, name = os.path.split(url)
    dst_path = os.path.join(gradle_dir, name)
    if os.path.exists(dst_path):
        print(f'file exist')
        return

    start_time = time.time()
    try:
        print(f'start download, dst: {dst_path}')
        response = requests.get(url, stream=True)  # 开启流式下载
        response.raise_for_status()  # 检查请求是否成功
        with open(dst_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):  # 分块写入
                file.write(chunk)
        print(f'download success, duration: {round(time.time() - start_time, 2)}s')
    except requests.RequestException as e:
        os.remove(dst_path)
        print(f'download fail, duration: {round(time.time() - start_time, 2)}s, e: {e}', file=sys.stderr)


def calculate_sha256(path):
    sha256_hash = hashlib.sha256()
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(8192), b''):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


if __name__ == '__main__':
    URL = 'https://services.gradle.org/distributions/'  # 替换为目标 URL
    fetch_gradle_distributions(URL)
