import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无界面模式
    service = Service('/Users/zhouzhenliang/bin/chromedriver-mac-x64/chromedriver')
    service.start()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    service = Service('/Users/zhouzhenliang/bin/chromedriver-mac-x64/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://www.google.com/')

    time.sleep(5)
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()

    time.sleep(50000)
    driver.quit()
