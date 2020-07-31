import scrapy
from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerProcess
from scrapy import spiderloader
import sys
from news.middlewares import wordSet
from news.models import News, db_connect, create_table
import scrapy.crawler as crawler
from multiprocessing import Process, Queue, Manager
from twisted.internet import reactor
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from pythainlp.util import isthai


def run_spider(spider, setting, search_value, alreadyUsedWordList, notYetUsedWordList):

    q = Queue()
    p = Process(target=f, args=(
        q, alreadyUsedWordList, notYetUsedWordList, setting, spider, search_value))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


def f(q, alreadyUsedWordList, notYetUsedWordList, setting, spider, search_value):
    try:
        runner = crawler.CrawlerRunner(setting)
        # deferred = runner.crawl(spider, search_field=search_value)
        # deferred.addBoth(lambda _: reactor.stop())
        for spider in spiderloader.SpiderLoader.from_settings(setting).list():
            runner.crawl(spider, search_field=search_value)

        deferred = runner.join()
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        print('In multi')
        print(wordSet)
        for word in wordSet:
            if word not in alreadyUsedWordList and word not in notYetUsedWordList:
                notYetUsedWordList.append(word)
        q.put(None)
    except Exception as e:
        q.put(e)


def run_everything():
    setting = get_project_settings()
    # process = CrawlerProcess(setting)
    alreadyUsedWord = Manager().list()
    notYetUsedWord = Manager().list()
    roundCount = 0
    # get json, input the search value from flask to here.
    search_field = sys.argv[1]
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    initialNewsCount = 0
    duplicateCountBeforeBreak = 0
    while True:
        alreadyUsedWord.append(search_field)
        run_spider('thai_spider', setting, search_field,
                   alreadyUsedWord, notYetUsedWord)
        session.commit()
        newsCount = session.query(func.count(News.id)).scalar()

        print('total news in db is' + str(newsCount))
        roundCount += 1
        if newsCount-initialNewsCount < 3:
            print("Too low news now let's stop")
            duplicateCountBeforeBreak +=1
            if duplicateCountBeforeBreak >= 2:
                break
        else:
            initialNewsCount = newsCount
            duplicateCountBeforeBreak = 0
        if len(notYetUsedWord) == 0:
            break
        search_field = notYetUsedWord.pop()

if __name__ == '__main__':
    run_everything()