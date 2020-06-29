from .models import News, Tag, News_tag
from . import db
from datetime import timedelta
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app, make_response
from flask_cors import CORS, cross_origin
from functools import update_wrapper
from collections import deque
import subprocess
import threading
# import crochet
# crochet.setup()

main = Blueprint('main', __name__)
# CORS(main, supports_credentials=True)
# main.config['CORS_HEADERS'] = 'Content-Type'
output_data = []
scrape_in_progress = False
scrape_complete = False
queue = deque()


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def progressFinishCheck():
    global scrape_in_progress
    global queue
    if len(queue) == 0:
        scrape_in_progress = False
    print('gets called')


def popenAndCall(onExit, *popenArgs, **popenKWArgs):
    """
    Runs a subprocess.Popen, and then calls the function onExit when the
    subprocess completes.
    Use it exactly the way you'd normally use subprocess.Popen, except include a
    callable to execute as the first argument. onExit is a callable object, and
    *popenArgs and **popenKWArgs are simply passed up to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs, popenKWArgs):
        proc = subprocess.Popen(*popenArgs, **popenKWArgs)
        proc.wait()
        onExit()
        return

    thread = threading.Thread(target=runInThread,
                              args=(onExit, popenArgs, popenKWArgs))
    thread.start()

    return thread  # returns immediately after the thread starts


# @main.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin',
#                          'http://localhost:3000')
#     response.headers.add('Access-Control-Allow-Headers',
#                          'Content-Type, Authorization')
#     response.headers.add('Access-Control-Allow-Methods',
#                          'GET,PUT,POST,DELETE,OPTIONS')
#     response.headers.add('Access-Control-Allow-Credentials', 'true')
#     return response


@main.route('/scraping', methods=['POST'])
# @cross_origin(allow_headers=['Content-Type'])
# @crossdomain(origin='')
def hello_world():
    global scrape_in_progress
    global scrape_complete
    global queue
    search_keyword = request.get_json()
    print(search_keyword)
    search_field = search_keyword['search_field']
    print(search_field)
    # search_field = request.args.get('search_field')
    queue.append(search_field)
    if not scrape_in_progress:
        scrape_in_progress = True
        while len(queue) > 0:
            field = queue.pop()
            # X-Doubt: not sure how this will work out when deploying.
            # popenAndCall(progressFinishCheck, ['ls'], cwd='./spider')
            popenAndCall(progressFinishCheck, [
                         'python', 'run_spiders.py', field], cwd='./spider')
    return 'SCRAPE IN PROGRESS'


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
