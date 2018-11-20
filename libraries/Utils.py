import json
from elasticsearch import Elasticsearch
import hashlib

class Utils:
    @staticmethod
    def obj_json_result(obj):
        return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def get_es_client():
        #es = Elasticsearch(
        #    ['106.14.21.227', '106.14.20.45'],
        #    http_auth=('elastic', 'elastic'),
        #    port=9200,
        #)
        es = Elasticsearch(['es.maimob.net:80'])
        return es

    @staticmethod
    def str_md5(data):
        return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()

    @staticmethod
    def log(content):
        with open('/data/logs/xfjr_bg_task/info.log','a') as f:
            f.write(content)
