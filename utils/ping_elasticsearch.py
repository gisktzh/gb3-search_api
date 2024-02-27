import time
from elasticsearch import Elasticsearch

def ping_elasticsearch(es: Elasticsearch):
    while True:
        es.ping()
        time.sleep(3600)
