import scrapy
import pandas as pd
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re

class VersionParser(scrapy.Spider):
    # Определяем URL, с которого начинаем парсинг
    url = 'https://www.ozon.ru/category/elektronika-7533/smartfony-i-smart-chasy-6921/'
    name = 'ozon_parser'
    allowed_domains = ['ozon.ru']
    start_urls = [
        url + '?from_home_goods=home_goods&from_filter=nosort&sort=relevance'
    ]

    custom_settings = {
        "SELENIUM_DRIVER_NAME": "chrome",
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy.downloadermiddlewares.httpauth.HttpAuthDownloadHandler",
            "https": "scrapy.downloadermiddlewares.redirect.RedirectDownloadHandler",
            "scrapy.exporters.CsvExporter": "scrapy_selenium.s3.S3DownloadHandler"
        },
        "FEED_EXPORTERS": {
            'csv': 'scrapy_selenium.s3.S3FeedExporter',
        },
    }

    def __init__(self, *args, **kwargs):
        self.driver = self.init_driver()
        super(VersionParser, self).__init__(*args, **kwargs)

    @staticmethod
    def init_driver():
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_settings.popups": 0,
            'profile.managed_default_content_settings.notifications': 2
        }
        options.add_experimental_option('prefs', prefs)
        return webdriver.Chrome(options=options)

    def parse(self, response, **kwargs):
        for link in response.css('.productCardInfo__link'):
            title = link.css('a::text').get()
            link_url = response.urljoin(link.xpath('@href').get())
            yield SeleniumRequest(
                url=link_url,
                callback=self.parse_product,
                cb_kwargs=dict(title=title),
                wait_time=1
            )

    def parse_product(self, response, title):
        operating_system = response.xpath('//div[@class="deviceItem__os"]/text()').get()
        if operating_system:
            operating_system = operating_system.strip()
        else:
            operating_system = "Unknown"
        try:
            rating = int(response.xpath('//span[@class="productRating__ratingValue"]/text()').get())
        except:
            rating = 0
        yield {
            'Title': title,
            'Version': operating_system,
            'Rating': rating,
        }

    def parse_top_100(self, response):
        products = response.css('div.productCard')
        for product in products:
            title = product.css('h3.productCard__title::text').get().split()[0]
            link_url = response.urljoin(product.xpath('.//a[@class="productCard__link"]/@href').get())
            yield SeleniumRequest(
                url=link_url, 
                callback=self.parse_product, 
                cb_kwargs=dict(title=title), 
                wait_time=5
            )

    def start_requests(self):
        self.driver.get(self.url)
        url = self.url
        page = self.driver.find_element_by_tag_name('html')
        scroll_height = self.driver.execute_script("return arguments[0].scrollHeight;", page)
        start = 0
        while True:
            self.driver.set_window_size(1920, 1080)
            page.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            if self.driver.execute_script('return document.body.scrollHeight;') == scroll_height:
                break
            start += 1
            yield scrapy.Request(url=url, callback=self.parse_top_100, meta={'start': start})

if __name__ == "__main__":  
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    process.crawl(VersionParser)
    process.start()
