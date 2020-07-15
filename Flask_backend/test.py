import json
import os
import unittest
from datetime import datetime
from unittest import mock
from api import app,db,models
from spider.news.models import News
from api.views import news_gather

class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
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
        self.assertEqual(actualnews['title'],test_news.title)
        # print(actualnews)

    @mock.patch("api.views.News")
    def test_filter(self, mock_news):
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


if __name__ == "__main__":
    unittest.main()