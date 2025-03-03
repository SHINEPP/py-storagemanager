from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from mp3.mysql_connection import open_mysql


class Mp3Distributions:

    def __init__(self):
        self.driver = None

    def start(self):
        # chromedriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无界面模式
        service = Service('/Users/zhouzhenliang/bin/chromedriver-mac-x64/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        for page in range(2166, 2168):
            distributions = self._fetch_distributions(page)
            print(f'distributions count: {len(distributions)}')
            for dist in distributions:
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

        self.driver.quit()

    def _fetch_distributions(self, page):
        distributions = []

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
                distributions.append(item)
                print(f'item = {item}')

        return distributions


if __name__ == '__main__':
    impl = Mp3Distributions()
    impl.start()
