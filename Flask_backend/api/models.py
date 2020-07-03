from . import db


class News(db.Model):
    __tablename__ = "news"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('news_topic', db.Text())
    body = db.Column('news_content', db.Text())
    date = db.Column('date', db.Text())  # Date
    author = db.Column('author', db.Text())
    url = db.Column('url', db.Text())
    category = db.Column('category', db.Text())
    # rawhtml = db.Column('rawhtml',Text(14294000000))
    # tags = db.relationship('Tag', secondary='news_tag',
    #                        lazy='dynamic', backref="news")  # M-to-M for quote and tag


class News_tag(db.Model):
    __tablename__ = "news_tags"
    __table_args__ = {'extend_existing': True}
    news_id = db.Column('news_id', db.Integer, primary_key=True)
    tag_id = db.Column('tag_id', db.Integer, primary_key=True)


class Tag(db.Model):
    __tablename__ = "tag"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(200), unique=True)
    # quotes = db.relationship('News', secondary='news_tag',
    #                          lazy='dynamic', backref="tag")  # M-to-M for quote and tag
