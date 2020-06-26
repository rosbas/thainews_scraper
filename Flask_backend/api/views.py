# from .models_movie import Movie
from .models import News, Tag, News_tag
from . import db
# from .scrapyTesting.thairath.main import
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
# import crochet
# crochet.setup()

main = Blueprint('main', __name__)
output_data = []


@main.route('/news')
def news_gather():
    news_list = News.query.all()
    news_array = []

    for one in news_list:
        news_array.append({'id': one.id, 'title': one.title, 'body': one.body, 'date': one.date,
                           'author': one.author, 'url': one.url, 'category': one.category  # , 'tags': one.tags ##
                           })
    return jsonify({'news': news_array})


# Tutorial for ez to understand
# @main.route('/add_movie', methods=['POST'])
# def add_movie():
#     movie_data = request.get_json()

#     new_movie = Movie(title=movie_data['title'], rating=movie_data['rating'])

#     db.session.add(new_movie)
#     db.session.commit()

#     return 'Done', 201


# @main.route('/movies')
# def movies():
#     movie_list = Movie.query.all()
#     movies = []

#     for movie in movie_list:
#         movies.append({'title': movie.title, 'rating': movie.rating})

#     return jsonify({'movies': movies})
