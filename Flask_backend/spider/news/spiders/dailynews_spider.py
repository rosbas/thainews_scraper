# -*- coding: utf-8 -*-
from pytz import timezone, all_timezones
import re
import scrapy
from datetime import datetime
from urllib.parse import quote
from time import sleep
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from..items import NewsItem


class DalinewsSpiderSpider(scrapy.Spider):
    name = 'dailynews_spider'
    start_urls = []
    current_page = 0
    query_pages = 0
    search_field = ""
    allowed_domains = []

    max_searching_page = 1
    max_query_pages = 5

    def start_requests(self):
        self.search_field = getattr(self, "search_field", "")
        yield scrapy.Request("https://www.dailynews.co.th/search?q=" + quote(self.search_field), callback=self.parse)

    def parse(self, response):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
        driver.get("https://www.dailynews.co.th/search?q=" +
                   quote(self.search_field))
        self.current_page += 1
        while self.current_page <= self.max_searching_page:
            self.current_page += 1
            scrapy_selector = Selector(text=driver.page_source)
            link_pages = scrapy_selector.css(
                'div.gsc-thumbnail-inside div.gs-title a.gs-title::attr(href)').extract()
            for page in link_pages:
                self.query_pages += 1
                if self.query_pages > self.max_query_pages:
                    return
                print(page)
                yield scrapy.Request(page, callback=self.parse_scrape_page, dont_filter=True)
                sleep(2)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[aria-label='หน้า " + str(self.current_page) + "']")))
            next_page = driver.find_element_by_css_selector(
                "div[aria-label='หน้า " + str(self.current_page) + "']")
            next_page.click()
            sleep(2)
        driver.close()

    def parse_scrape_page(self, response):
        items = NewsItem()
        title = response.css('.title::text').extract_first()
        if title is None:
            return
        author = "dailynews"
        date_notformat = response.css('.date::text').extract_first()
        date = DalinewsSpiderSpider.date_format(date_notformat)
        title_description = response.css('.desc::text').extract_first()
        body_description = response.css(
            '.entry.textbox.content-all::text').extract()
        empty_string = ''
        body_all = empty_string.join(body_description)
        body = " ".join((title_description + body_all).split())
        category = DalinewsSpiderSpider.get_tags(response.url)
        url = response.url
        # html_source = response.txt

        items['title'] = title
        items['author'] = author
        items['date'] = date
        items['body'] = body
        items['category'] = category
        items['url'] = url
        # items['html_source'] = html_source
        yield items

    def get_tags(link):
        pattern = ".co.th/(.*?)/"
        substring = re.search(pattern, link).group(1)
        return substring

    def date_format(date_string):
        re_date = date_string.replace("ที่", "").replace(
            "เวลา", "").replace("น.", "")
        thai_full_weekdays = [
            "จันทร์",
            "อังคาร",
            "พุธ",
            "พฤหัสบดี",
            "ศุกร์",
            "เสาร์",
            "อาทิตย์",
        ]
        thai_full_months = [
            "มกราคม",
            "กุมภาพันธ์",
            "มีนาคม",
            "เมษายน",
            "พฤษภาคม",
            "มิถุนายน",
            "กรกฎาคม",
            "สิงหาคม",
            "กันยายน",
            "ตุลาคม",
            "พฤศจิกายน",
            "ธันวาคม",
        ]
        for i in thai_full_weekdays:
            re_date = re_date.replace(i, "")
        re_date = re_date.strip(" ")
        date_split = re_date.split()
        year = int(date_split[2]) - 543
        month = thai_full_months.index(date_split[1]) + 1
        day = date_split[0]
        hour = date_split[3][0:2]
        minute = date_split[3][3:5]
        datetime_object = datetime(year=int(year), month=int(month), day=int(
            day), hour=int(hour), minute=int(minute), second=0)
        tz = timezone('Asia/Bangkok')
        fmt = '%Y-%m-%d %H:%M:%S'
        loc_dt = tz.localize(datetime_object)
        return loc_dt.strftime(fmt)
