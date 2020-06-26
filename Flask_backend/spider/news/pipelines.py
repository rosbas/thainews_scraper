# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from .models import News, Tag, db_connect, create_table

class ThairathPipeline:

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        session = self.Session()
        tag = Tag()
        news = News()
        for key in dict(item).keys():

            if key != "tags" :
                news[key]=item[key]
        # news.author = item["author"]
        # news.news_topic = item["title"]
        # news.news_content = item["body"]
        # news.date = item["date"]
        # news.url = item["url"]
        # news.category=item["category"]
        # news.rawhtml=item["rawhtml"]
        if "tags" in item:
            for tag_name in item["tags"]:
                tag = Tag(name=tag_name)
                exist_tag = session.query(Tag).filter_by(name=tag.name).first()
                if exist_tag is not None:  # the current tag exists
                    tag = exist_tag
                news.tags.append(tag)
        try:
            session.add(news)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()
        return item

class DuplicatesPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()

        exist_news = session.query(News).filter_by(url=item["url"]).first()
        if exist_news is not None:  # the current quote exists
            raise DropItem("Duplicate item found: %s" % item["url"])
            session.close()
        else:
            return item
            session.close()