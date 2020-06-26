# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem
from urllib.parse import quote,urlparse
from datetime import datetime
from pytz import timezone, all_timezones

class ThaiRathSpider(scrapy.Spider):
    name = 'thai_spider'
    search_field = "ิ"
    count_page = 0
    max_page = 5
    start_urls = []
    allowed_domains = ["thairath.co.th"]
    def start_requests(self):
        # self points to the spider instance
        # that was initialized by the scrapy framework when starting a crawl
        #
        # spider instances are "augmented" with crawl arguments
        # available as instance attributes,
        # self.ip has the (string) value passed on the command line
        # with `-a ip=somevalue`
        self.search_field = getattr(self,"search_field","")

        yield scrapy.Request('https://www.thairath.co.th/search?q='+quote(self.search_field)+'&p=1', callback=self.parse)
    def parse(self, response):
        content_page = response.css(".col-8 a").css("::attr(href)").extract()
        if len(content_page) ==0:
            return
        for page in content_page:
            yield scrapy.Request(page, callback= self.parse_item)
        self.count_page +=1
        next_page = "https://www.thairath.co.th/search?q=" +quote(self.search_field)+'&p='+str(self.count_page+1)
        if self.count_page < self.max_page:
            yield scrapy.Request(next_page, callback= self.parse)


    def parse_item(self, response):
        items = NewsItem()
        title = response.css(".e1ui9xgn0::text").extract_first()
        author = response.css(".e1ui9xgn1 a").css("::text").extract_first()
        date = response.css(".e1ui9xgn2::text").extract_first()
        body = response.css("p , strong").css("::text").extract()
        bodytext = ""
        for paragraph in body:
            bodytext += paragraph + " /p "
        bodytext.strip()
        tags = response.css(".evs3ejl15 a").css("::text").extract()
        url = response.request.url
        items['title'] = title
        items['author'] = author
        items['date'] = self.parse_date(date)
        items['body'] = bodytext
        items['tags'] = tags
        items['url'] = url
        items['category'] = self.parse_category(url,2)
        # items['rawhtml'] = response.text
        yield items

    def parse_date(self,input_date):
        date = input_date.replace("\xa0", " ")
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
        day = splitlist[0]
        month = str(thai_abbr_months.index(splitlist[1]) + 1)
        year = str(int(splitlist[2]) - 543)
        time = splitlist[3].replace("น.", "")
        hour = (time.split(":"))[0]
        minute = (time.split(":"))[1]
        d = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), )
        tz = timezone('Asia/Bangkok')
        fmt = '%Y-%m-%d %H:%M:%S'
        loc_dt = tz.localize(d)
        return  loc_dt.strftime(fmt)
    def parse_category(self,url,indexOfCategory):
        o = urlparse(url)
        splitlist = o.path.split("/")
        category = splitlist[indexOfCategory]
        return category
