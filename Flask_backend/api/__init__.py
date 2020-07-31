import os

import sqlalchemy
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
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL",
                                                      "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8".format(
            drivername="mysql",
            user="user",
            passwd="password",
            host="mysql",
            port="8080",
            db_name="db",
            # drivername="postgresql",

        ))

    # //for scrapy
    if os.getenv("IS_GOOGLE"):
        print("running in google")
        print(os.environ["DB_USER"])
        app.config['SQLALCHEMY_DATABASE_URI'] =sqlalchemy.engine.url.URL(
                                                    drivername='mysql+pymysql',
                                                    username=os.environ["DB_USER"],
                                                    password=os.environ["DB_PASS"],
                                                    database=os.environ["DB_NAME"],
                                                    query={
                                                        'unix_socket': '/cloudsql/{}'.format(os.environ["CLOUD_SQL_CONNECTION_NAME"])
                                                    }
                                                )
          # "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8".format(
            # drivername="mysql",
            # user="user",
            # passwd="password",
            # host="mysql",
            # port="8080",
            # db_name="db",))

    app.config['CORS_HEADERS'] = 'Content-Type'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    pymysql.install_as_MySQLdb()
    db.init_app(app)

    from .views import main,start_up
    app.register_blueprint(main)
    if app.config['TESTING'] == False:
        start_up()
    return app

app=create_app()