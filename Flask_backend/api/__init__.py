from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}
         )

    # //for scrapy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scrapy_quotes.db'
    app.config['CORS_HEADERS'] = 'Content-Type'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    from .views import main
    app.register_blueprint(main)

    return app
app=create_app()