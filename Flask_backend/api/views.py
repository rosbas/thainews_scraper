from .models import News, Tag, News_tag
from . import db
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
import subprocess
import threading
from collections import deque
# import crochet
# crochet.setup()

main = Blueprint('main', __name__)
output_data = []
scrape_in_progress = False
scrape_complete = False
queue = deque()


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


@main.route('/scraping', methods=['POST'])
def hello_world():
    global scrape_in_progress
    global scrape_complete
    global queue
    # search_keyword = request.get_json()
    # print(search_keyword)
    # search_field = search_keyword['search_field']
    search_field = "คสช"
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
