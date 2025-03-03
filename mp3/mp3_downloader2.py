import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from mp3.mysql_connection import open_mysql


class Mp3Detail:

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

        sql = 'SELECT detail_url FROM audio_kumeiwp LIMIT 5'
        with open_mysql() as cursor:
            cursor.execute(sql)
            for row in cursor:
                detail_url = row[0]
                print(f'detail_url = {detail_url}')
                title, download_url = self._parse_detail_page(detail_url)
                if title and download_url:
                    print(f'{title}: {download_url}')

        self.driver.quit()

    def _parse_detail_page(self, detail_url):
        self.driver.get(detail_url)
        layout_box = self.driver.find_element(By.CLASS_NAME, 'layout_box')
        if not layout_box:
            return None, None
        layui_card = layout_box.find_element(By.CLASS_NAME, 'layui-card')
        if not layui_card:
            return None, None
        wai1s = layui_card.find_elements(By.CLASS_NAME, 'wai1')
        if wai1s and len(wai1s) == 4:
            item1 = wai1s[0]
            values = item1.find_elements(By.TAG_NAME, 'div')
            if values and len(values) == 2:
                title = values[0].text.strip()
                download_url = values[1].text.strip()
                return title, download_url
        return None, None


if __name__ == '__main__':
    impl = Mp3Detail()
    impl.start()
