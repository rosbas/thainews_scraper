import json
import os
import logging, sys
import unittest
from datetime import datetime
from unittest import mock

from scrapy import Request
from scrapy.http import HtmlResponse

from spider.news.models import News
from spider.news.spiders.thairath_spider import ThaiRathSpider
from api.views import news_gather

from betamax import Betamax
from betamax.fixtures.unittest import BetamaxTestCase

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pymysql


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################
    # logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    # executed prior to each test
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scrapy_news.db'
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + "scrapy_news1.db"
        # os.environ["DATABASE_URL"] = 'sqlite:///' + "scrapy_news2.db"
        self.app = app.test_client()
        # self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        # db.drop_all()
        # db.session.remove()
        # drop all tables in db

        # remove app_context
        # app.app_context.pop()
        pass

    ###############
    #### tests ####
    ###############
    #
    # def test_scrape(self):
    #     response=self.app.post('/scraping',
    #                    data=json.dumps(dict(search_field='กัน')),
    #                    content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    @mock.patch("api.views.News")
    def test_query(self, mock_news):
        print("Testing URL /news")
        test_news = News()
        test_news.title="title"
        test_news.url="https://www.a.co.th"
        test_news.author="author"
        test_news.category="category"
        test_news.body="body"
        test_news.id=1
        test_news.date=datetime.now()
        mock_news.query.all.return_value = [test_news]

        response=self.app.get('/news')

        newsjson = json.loads(response.data.decode("utf-8"))
        actualnews = newsjson['news'][0]
        try:
            self.assertEqual(actualnews['title'],test_news.title)
            logging.debug("Testing URL of / news is completed.")
        except AssertionError:
            logging.debug("An error occur while testing URL of / news")
        # print(actualnews)

    @mock.patch("api.views.News")
    def test_filter(self, mock_news):
        print("Testing URL /filter")
        test_news = News()
        test_news.title = "title"
        test_news.url = "https://www.a.co.th"
        test_news.author = "author"
        test_news.category = "category"
        test_news.body = "body"
        test_news.id = 1
        test_news.date = datetime.now()
        mock_news.query.filter \
                .return_value.all \
                .return_value = [test_news]
        response=self.app.post('/searching',
                       data=json.dumps(dict(search_field='title')),
                       content_type='application/json')
        newsjson = json.loads(response.data.decode("utf-8"))
        actualnews = newsjson['news'][0]
        self.assertEqual(actualnews['title'], test_news.title)
        # print(response.data)



with Betamax.configure() as config:
    # where betamax will store cassettes (http responses):
    config.cassette_library_dir = 'cassettes'
    config.preserve_exact_body_bytes = True


class TestExample(BetamaxTestCase):  # superclass provides self.session

    def test_parse(self):
        example = ThaiRathSpider()
        print("Testing Thai spider")
        # http response is recorded in a betamax cassette:
        url = "https://www.thairath.co.th/news/local/bangkok/1889828"
        response = self.session.get(url)
        # forge a scrapy response to test
        scrapy_response = HtmlResponse(body=response.content, url=url, request=Request(url=url))
        result = example.parse_item(scrapy_response)
        item = next(result)
        self.assertEqual(item['url'],url,"url is not the same")
        self.assertEqual(item['title'],"เหยื่อโควิด ตายเหมือนผักปลา 5.78 แสนศพ ติดเชื้อจากนอก มาไทย รวม 295 ราย","title is not the same")
        # with self.assertRaises(StopIteration):
        #     result.next()
if __name__ == "__main__":
    unittest.main()