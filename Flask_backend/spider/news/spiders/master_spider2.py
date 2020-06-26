# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerRunner
# from scrapy import spiderloader
# from twisted.internet import reactor, defer
#
# class MasterSpider2(scrapy.Spider):
#     name = 'master_spider2'
#     search_field = "ิ"
#     start_urls = []
#     def start_requests(self):
#         # self points to the spider instance
#         # that was initialized by the scrapy framework when starting a crawl
#         #
#         # spider instances are "augmented" with crawl arguments
#         # available as instance attributes,
#         # self.ip has the (string) value passed on the command line
#         # with `-a ip=somevalue`
#         self.search_field = getattr(self,"search_field","")
#         yield scrapy.Request("http://quotes.toscrape.com", callback=self.parse)
#
#
#     def parse(self, response):
#         return self.justanotherfunc()
#     def justanotherfunc(self):
#         setting = get_project_settings()
#         spider_loader = spiderloader.SpiderLoader.from_settings(setting)
#         runner = CrawlerRunner(setting)
#
#         @defer.inlineCallbacks
#         def crawl():
#             yield runner.crawl("thai_spider", search_field=self.search_field)
#             reactor.stop()
#
#         crawl()
#         reactor.run()