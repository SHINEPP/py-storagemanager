import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class AppDetail:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        name = self.soup.find(attrs={'itemprop': 'name'})
        star_rating = self.soup.find(attrs={'itemprop': 'starRating'})
        content_rating = self.soup.find(attrs={'itemprop': 'contentRating'})
        offers = self.soup.find(attrs={'itemprop': 'offers'})
        price = self.soup.find(attrs={'itemprop': 'price'})
        description = self.soup.find(attrs={'itemprop': 'description'})
        genre = self.soup.find(attrs={'itemprop': 'genre'})
        print(f'name: {name.text.strip()}')
        print(f'star_rating: {star_rating.text.strip()}')
        print(f'content_rating: {content_rating}')
        print(f'offers: {offers}')
        print(f'price: {price}')
        print(f'description: {description}')
        print(f'genre: {genre}')


def main():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument("--lang=en-US")
    options.add_argument("--timezone=America/New_York")
    service = Service('/Users/zhouzhenliang/bin/chromedriver-mac-x64/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://play.google.com/store/apps/details?id=qrcodereader.barcodescanner.scan.qrscanner')
    html = driver.page_source
    time.sleep(100000)
    driver.quit()
    AppDetail(html)


if __name__ == '__main__':
    main()
    with open('temp.txt', 'r') as file:
        AppDetail(file.read())
