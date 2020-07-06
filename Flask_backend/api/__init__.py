import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pymysql

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # is this secure, someone helpppp
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    # //for scrapy
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL",
    #                                                   'sqlite:///scrapy_news.db')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8".format(
            drivername="mysql",
            user="root",
            passwd="diluggmkLn4NhJuv",
            host="35.224.148.74",
            port="3306",
            db_name="db") #don't have db name yet.
    # 'mysql://root:diluggmkLn4NhJuv@35.224.148.74:3306/database.db'
    pymysql.install_as_MySQLdb()
    db.init_app(app)

    from .views import main
    app.register_blueprint(main)

    return app

app=create_app()