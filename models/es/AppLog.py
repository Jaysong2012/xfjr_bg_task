from libraries.Utils import Utils
from libraries.Constants import RETURN_CODE_MSG_ENUM_DICT
class AppLog:

    index   = 'app_log'

    @classmethod
    def get_range_general(cls,gte,lte,ranges):
        es = Utils.get_es_client()
        query = {
            "query": {
                "bool": {
                    "filter": {
                        "range": {
                            "request.baseRequest.timeStamp": {
                                "gte": gte,
                                "lte": lte
                            }
                        }
                    }
                }
            },
            "aggs": {
                "timestamp_range": {
                    "range": {
                        "field": "request.baseRequest.timeStamp",
                        "keyed": "true",
                        "ranges": ranges
                    },
                    "aggs": {
                        "call_terms": {
                            "terms": {
                                "field": "request.baseRequest.call.keyword",
                                "size": 100
                            },
                            "aggs": {
                                "terms_returnCode": {
                                    "terms": {
                                        "field": "response.returnCode.keyword",
                                        "size": 100
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        print(query)
        try:
            res = es.search(index=cls.index, doc_type=cls.index, body=query)
        except Exception as e:
            print('查询失败 ',e)
            res = None
        if res == None:
            return
        buckets = res['aggregations']['timestamp_range']['buckets']
        time_key_report_list = []
        for k, v in buckets.items():
            hour_report = {}
            hour_report['time_key'] = k
            hour_report['from'] = v['from']
            hour_report['to'] = v['to']
            hour_report['doc_count'] = v['doc_count']
            call_stat_list = []
            call_stat_buckets = v['call_terms']['buckets']
            for bucket in call_stat_buckets:
                call_detail = {}
                return_detail_list = []
                call_detail['call'] = bucket['key']
                call_detail['call_num'] = bucket['doc_count']
                returncode_buckets = bucket['terms_returnCode']['buckets']
                for returncode_bucket in returncode_buckets:
                    return_detail = {}
                    return_detail['return_code'] = returncode_bucket['key']
                    return_detail['return_msg'] = RETURN_CODE_MSG_ENUM_DICT.get(str(returncode_bucket['key']), 'UnKnow')
                    return_detail['return_num'] = str(returncode_bucket['doc_count']) + '    ('+str(int(int(returncode_bucket['doc_count']) * 100 / int(bucket['doc_count'])))+'%)'
                    return_detail_list.append(return_detail)
                call_detail['return_stat'] = return_detail_list
                call_stat_list.append(call_detail)
            hour_report['call_stat'] = call_stat_list
            time_key_report_list.append(hour_report)
        return time_key_report_list

    @classmethod
    def get_timestamp_range_general(cls,gte,lte):
        report = {}
        report['gte'] = gte
        report['lte'] = lte
        es = Utils.get_es_client()
        query = {
            "query": {
                "bool": {
                    "filter": {
                        "range": {
                            "request.baseRequest.timeStamp": {
                                "gte": gte,
                                "lte": lte
                            }
                        }
                    }
                }
            },
            "aggs": {
                "call_terms": {
                    "terms": {
                        "field": "request.baseRequest.call.keyword",
                        "size": 100
                    },
                    "aggs": {
                        "terms_returnCode": {
                            "terms": {
                                "field": "response.returnCode.keyword",
                                "size": 100
                            }
                        }
                    }
                }
            }
        }
        try:
            res = es.search(index=cls.index, doc_type=cls.index, body=query)
        except Exception as e:
            res = None
            print(' 查询失败 ' , e )
        if res == None:
            return
        buckets = res['aggregations']['call_terms']['buckets']
        print(type(buckets))
        call_stat_list = []
        for bucket in buckets:
            call_detail = {}
            return_detail_list = []
            call_detail['call'] = bucket['key']
            call_detail['call_num'] = bucket['doc_count']
            returncode_buckets = bucket['terms_returnCode']['buckets']
            for returncode_bucket in returncode_buckets:
                return_detail = {}
                return_detail['return_code'] = returncode_bucket['key']
                return_detail['return_msg'] = RETURN_CODE_MSG_ENUM_DICT.get(str(returncode_bucket['key']),'UnKnow')
                return_detail['return_num'] = returncode_bucket['doc_count']
                return_detail_list.append(return_detail)
            call_detail['return_stat'] = return_detail_list
            call_stat_list.append(call_detail)
        report['call_stat'] = call_stat_list
        return report
