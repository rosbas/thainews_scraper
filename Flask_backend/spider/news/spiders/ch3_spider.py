# -*- coding: utf-8 -*-
import scrapy
from time import sleep
from scrapy.selector import Selector
from ..items import NewsItem
from urllib.parse import quote, urlparse, unquote
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from pytz import timezone, all_timezones
import os

class Ch3Spider(scrapy.Spider):
    name = 'ch3_spider'
    search_field = "ิ"
    count_page = 0
    max_page = 5
    start_urls = []
    allowed_domains = ["news.ch3thailand.com"]
    def start_requests(self):
        # self points to the spider instance
        # that was initialized by the scrapy framework when starting a crawl
        #
        # spider instances are "augmented" with crawl arguments
        # available as instance attributes,
        # self.ip has the (string) value passed on the command line
        # with `-a ip=somevalue`
        self.search_field = getattr(self,"search_field","")
        yield scrapy.Request("https://www.ch3thailand.com/search?q=" + quote(self.search_field), callback=self.parse)


    def parse(self, response):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument("--no-sandbox")
        op.add_argument("--disable-setuid-sandbox")
        op.add_argument("--disable-extensions")
        if os.getenv('IS_APP_ENGINE'):
            driver = webdriver.Chrome(chrome_options=op)
        else:
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
        driver.get("https://www.ch3thailand.com/search?q=" + quote(self.search_field))
        self.count_page += 1
        while self.count_page < self.max_page:
            self.count_page += 1
            scrapy_selector = Selector(text=driver.page_source)
            content_page = scrapy_selector.css('.gs-title::attr(href)').extract()
            if len(content_page) == 0:
                return
            for page in content_page:
                yield scrapy.Request(page, callback=self.parse_item)
            next_page = driver.find_elements_by_css_selector("div[aria-label='หน้า " + str(self.count_page) + "']")
            if len(next_page) == 0:
                return
            next_page[0].click()
            print(self.count_page)
            sleep(5)
        driver.close()

    def parse_item(self, response):
        items = NewsItem()
        title = response.css(".content-head::text").extract_first()
        if title is None:
            return
        print(title)
        author = "ch3"
        date = response.css(".content-des-text:nth-child(2)::text").extract_first()
        body = response.css(".content-news").css("::text").extract()
        bodytext = ""
        for paragraph in body:
            bodytext += paragraph + " /p "
        bodytext.strip()
        tags = response.css(".content-tag-click").css("::text").extract()
        print(tags)
        print("\n")
        url = response.request.url
        items['title'] = title
        items['author'] = author
        items['date'] = self.parse_date(date)
        items['body'] = bodytext
        items['tags'] = tags
        items['url'] = url
        items['category'] = unquote(self.parse_category(url, 1))
        # items['rawhtml'] = response.text
        yield items

    def parse_date(self,input_date):
        date = input_date.replace("วันที่", "").replace("เวลา", "").replace("น.", "").replace("\xa0", " ")
        date = date.strip()
        splitlist = date.split(" ")
        thai_abbr_months = [
            "ม.ค.",
            "ก.พ.",
            "มี.ค.",
            "เม.ย.",
            "พ.ค.",
            "มิ.ย.",
            "ก.ค.",
            "ส.ค.",
            "ก.ย.",
            "ต.ค.",
            "พ.ย.",
            "ธ.ค.",
        ]
        splitlist.remove("")
        day = splitlist[0]
        month = str(thai_abbr_months.index(splitlist[1]) + 1)
        year = str(int(splitlist[2]) + 2500 - 543)
        time = splitlist[3].replace("น.", "")
        hour = (time.split(":"))[0]
        minute = (time.split(":"))[1]
        second = ((time.split(":"))[2])
        d = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute),
                     second=int(second))
        tz = timezone('Asia/Bangkok')
        fmt = '%Y-%m-%d %H:%M:%S'
        loc_dt = tz.localize(d)
        return loc_dt.strftime(fmt)
    def parse_category(self,url,indexOfCategory):
        o = urlparse(url)
        splitlist = o.path.split("/")
        category = splitlist[indexOfCategory]
        return category
