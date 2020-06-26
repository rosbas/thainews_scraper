# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem
from elasticsearch7 import Elasticsearch
from scrapy.utils.serialize import ScrapyJSONEncoder

class ElasticPipeline:
    encoder = ScrapyJSONEncoder()
    def __init__(self):
        self.es = connect_elasticsearch()
        create_index(self.es, 'newsdb')


    def process_item(self, item, spider):
        es = self.es

        # newsJSON = json.dumps(self.encoder.encode(item))
        newsJSON = json.loads(self.encoder.encode(item))
        print(newsJSON)
        if es is not None:
            if create_index(es, 'newsdb'):
                out = store_record(es, 'newsdb', newsJSON)
                print('Data indexed successfully')
        return item

class DuplicatesPipeline(object):
    def __init__(self):
        self.es = connect_elasticsearch()
        create_index(self.es,'newsdb')


    def process_item(self, item, spider):
        es = self.es
        # search_object = {'_source': ['url'], 'query': {'match': {'url': item['url']}}}
        search_object = json.dumps({
            '_source': ['url'],
            "query": {
                "match_phrase": {
                    "url": item['url']
                }
            }
        })
        res = search(es, 'newsdb', search_object)
        print(res)
        if len(res['hits']['hits'])==0:
            return item
        else:
            raise DropItem("Duplicate item found: %s" % item["url"])


def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)
    return res

def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
                "dynamic": "strict",
                "properties": {
                    "title": {
                        "type": "text"
                    },
                    "author": {
                        "type": "text"
                    },
                    "date": {
                        "type": "text"
                    },
                    "body": {
                        "type": "text"
                    },
                    "tags":{
                        "type": "text"
                    },
                    "category": {
                        "type": "text"
                    },
                    "url":{
                        "type": "text"
                    },

            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
           print(str(ex))
    finally:
        return created

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es

def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))