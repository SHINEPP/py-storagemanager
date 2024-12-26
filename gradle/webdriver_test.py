import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

if __name__ == '__main__':
    service = Service('/Users/zhouzhenliang/bin/chromedriver-mac-x64/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.google.com/')
    time.sleep(5)
    driver.quit()
