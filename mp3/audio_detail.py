from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from mp3.mysql_connection import open_mysql


class AudioDetailParser:

    def __init__(self):
        self.driver = None

    def start(self):
        # chromedriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无界面模式
        service = Service('/Users/zhouzhenliang/bin/chromedriver-mac-x64/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        sql = ('SELECT detail_url, name, upload_time '
               'FROM audio_kumeiwp A '
               'WHERE NOT EXISTS ('
               'SELECT 1 FROM audio_kumeiwp_detail B WHERE B.detail_url = A.detail_url'
               ')')
        with open_mysql() as cursor:
            cursor.execute(sql)
            for row in cursor:
                detail_url = row[0]
                print(f'detail_url = {detail_url}')
                title, download_url = self._parse_detail_page(detail_url)
                if title and download_url:
                    print(f'{title}: {download_url}')
                    parsed_url = urlparse(download_url)
                    path = parsed_url.path
                    sql2 = f'REPLACE INTO audio_kumeiwp_detail(detail_url,download_url,local_path) VALUES(%s,%s,%s)'
                    values = (detail_url, download_url, path)
                    with open_mysql() as cursor2:
                        cursor2.execute(sql2, values)

        self.driver.quit()

    def _parse_detail_page(self, detail_url):
        self.driver.get(detail_url)
        layout_box = self.driver.find_element(By.CLASS_NAME, 'layout_box')
        if not layout_box:
            return None, None
        layui_card = layout_box.find_element(By.CLASS_NAME, 'layui-card')
        if not layui_card:
            return None, None
        r = layout_box.find_element(By.CLASS_NAME, 'r')
        if not r:
            return None, None
        wai1s = r.find_elements(By.CLASS_NAME, 'wai1')
        if wai1s and len(wai1s) == 4:
            item1 = wai1s[0]
            values = item1.find_elements(By.TAG_NAME, 'div')
            if values and len(values) == 2:
                title = values[0].text.strip()
                download_url = values[1].text.strip()
                return title, download_url
        return None, None


if __name__ == '__main__':
    impl = AudioDetailParser()
    impl.start()
