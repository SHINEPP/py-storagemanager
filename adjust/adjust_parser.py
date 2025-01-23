import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class AppDetail:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        items = self.soup.find_all(attrs={'data-testid': 'app-tile'})
        for item in items:
            print(f'{item}')


def main():
    options = Options()
    # options.add_argument('--headless')
    service = Service('/Users/zhouzhenliang/bin/chromedriver-mac-x64/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://suite.adjust.com/apps')
    html = driver.page_source
    time.sleep(100000)
    driver.quit()
    # AppDetail(html)


if __name__ == '__main__':
    # main()
    with open('Adjust.html', 'r') as file:
        AppDetail(file.read())
