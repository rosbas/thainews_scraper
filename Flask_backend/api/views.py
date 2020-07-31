import signal
import time

from sqlalchemy.orm.state import InstanceState
from .models import News, Tag, News_tag

from flask import Blueprint, jsonify, request, Response

from collections import deque
import subprocess
import threading


main = Blueprint('main', __name__)
output_data = []
scrape_in_progress = False
scrape_complete = False
queue = deque()
proc = None

def progressFinishCheck():
    global scrape_in_progress
    global queue
    if len(queue) == 0:
        scrape_in_progress = False
    print('gets called')

def scheduleNextScrape():
    time.sleep(60*60*5)
    print('sleep for 5 hrs')
    start_up()


def popenAndCall(onExit, *popenArgs, **popenKWArgs):
    """
    Runs a subprocess.Popen, and then calls the function onExit when the
    subprocess completes.
    Use it exactly the way you'd normally use subprocess.Popen, except include a
    callable to execute as the first argument. onExit is a callable object, and
    *popenArgs and **popenKWArgs are simply passed up to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs, popenKWArgs):
        global proc
        proc = subprocess.Popen(*popenArgs, **popenKWArgs)
        print(type(proc))
        proc.wait()
        onExit()
        return

    thread = threading.Thread(target=runInThread,
                              args=(onExit, popenArgs, popenKWArgs))
    thread.start()

    return thread  # returns immediately after the thread starts

def start_up():
    search_field = 'ข่าว'
    popenAndCall(scheduleNextScrape, [
                 'python3', 'startup.py', search_field], cwd='./spider')
    # popenAndCall(progressFinishCheck, [
    #     'scrapy','crawl', 'thai_spider', '-a', 'search_field=ข่าว'], cwd='./spider/news/spiders')


@main.route('/scraping', methods=['POST'])
def hello_world():
    global scrape_in_progress
    global scrape_complete
    global queue
    search_keyword = request.get_json()
    search_field = search_keyword['search_field']
    # search_field = request.args.get('search_field')
    queue.append(search_field)
    if not scrape_in_progress:
        scrape_in_progress = True
        while len(queue) > 0:
            field = queue.pop()
            popenAndCall(progressFinishCheck, [
                         'python3', 'run_spiders.py', field], cwd='./spider')
            # popenAndCall(progressFinishCheck, [
            #     'scrapy','crawl', 'thai_spider', '-a', 'search_field=ข่าว'], cwd='./spider/news/spiders')
    return 'SCRAPE IN PROGRESS'


@main.route('/news')
def news_gather():
    try:
        news_list = News.query.all()
        news_array = []

        for one in news_list:
            news_array.append({'id': one.id, 'title': one.title, 'body': one.body, 'date': one.date,
                            'author': one.author, 'url': one.url, 'category': one.category  # , 'tags': one.tags ##
                            })
        return jsonify({'news': news_array})
    except:
        print("DB is not initilize")
        return "Database is not initilize"


@main.route('/news/csv')
def news_gatherCSV():
    try:
        news_list = News.query.all()
        # generateCSVFromSQLAlchemy(news_list,True)
        # return None
        return Response(generateCSVFromSQLAlchemy(news_list, True), mimetype='text/csv')
    except:
        print("DB is not initilize")
        return "Database is not initilize"

def generateCSVFromSQLAlchemy(sqlQueryList, withKeys):
    i = 0
    for one in sqlQueryList:
        if i == 0 and withKeys:

            yield ','.join(filter(lambda x: not x.startswith('_'), one.__dict__.keys()))+'\n'
            i += 1
        yield ','.join([(str(i).replace(",", ""))for i in filter(lambda x: not isinstance(x, InstanceState), one.__dict__.values())]) + '\n'


@main.route('/searching', methods=['POST'])
def searching():
    tag = request.args.get('search_field')
    search = "%{}%".format(tag)
    posts = News.query.filter(News.title.like(search)).all()
    news_array = []

    for one in posts:
        news_array.append({'id': one.id, 'title': one.title, 'body': one.body, 'date': one.date,
                           'author': one.author, 'url': one.url, 'category': one.category  # , 'tags': one.tags ##
                           })
    return jsonify({'news': news_array})



@main.route('/stop', methods=['POST'])
def stop_scraping():
    global proc
    if isinstance(proc,subprocess.Popen):
        if proc.poll() is None:
            # proc.kill()
            # outs, errs = proc.communicate()
            proc.send_signal(signal.SIGINT)
            proc.send_signal(signal.SIGINT)

            return 'Process stopped'
    return 'No Scraping is run'


@main.route('/status')
def get_status():
    global scrape_in_progress
    if scrape_in_progress:
        return 'Currently Scraping'
    return 'Currently Not Scraping'


@main.route('/queue')
def get_queue():
    global queue
    return str(queue)