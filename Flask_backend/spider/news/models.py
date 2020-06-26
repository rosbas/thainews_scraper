from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
import pymysql
import os

from .settings import SQLITE_FILE

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    # pymysql.install_as_MySQLdb()
    if not os.getenv("DATABASE_URL"):
        # raise RuntimeError("DATABASE_URL is not set")
        # CONNECTION_STRING = "sqlite:///scrapy_quotes.db"
        CONNECTION_STRING = "sqlite:///" + SQLITE_FILE
        print(CONNECTION_STRING)
        return create_engine(CONNECTION_STRING)
    else:
        return create_engine((os.getenv("DATABASE_URL")))


def create_table(engine):
    Base.metadata.create_all(engine)


# Association Table for Many-to-Many relationship between Quote and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
quote_tag = Table('news_tag', Base.metadata,
                  Column('news_id', Integer, ForeignKey('news.id')),
                  Column('tag_id', Integer, ForeignKey('tag.id'))
                  )


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column('news_topic', Text())
    body = Column('news_content', Text(400000))
    date = Column('date', Text())  # Date
    author = Column('author', Text())
    url = Column('url', Text())
    category = Column('category', Text())
    # rawhtml = Column('rawhtml',Text(14294000000))
    tags = relationship('Tag', secondary='news_tag',
                        lazy='dynamic', backref="news")  # M-to-M for quote and tag

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column('name', String(200), unique=True)
    quotes = relationship('News', secondary='news_tag',
                          lazy='dynamic', backref="tag")  # M-to-M for quote and tag
