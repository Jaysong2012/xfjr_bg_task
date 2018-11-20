# -*- coding:utf-8 -*-

from libraries.Mail import Mail
from libraries.Utils import Utils
from libraries.DateTimeUtil import DateTimeUtil
from models.es.AppLog import AppLog
import json

def json_repot(start_time,end_time,time_key_type=0):
    start_time = start_time+' 00:00:00'
    end_time = end_time +' 23:59:59'

    start_timestamp = DateTimeUtil.strtime_to_timestamp(start_time, '%Y-%m-%d %H:%M:%S')
    end_timstamp = DateTimeUtil.strtime_to_timestamp(end_time, '%Y-%m-%d %H:%M:%S')
    timestamp_duration = (1000 * 60 *60) if time_key_type == 1 else (1000 * 60 * 60 * 24)
    ranges = []

    for i in range(int((end_timstamp - start_timestamp)/timestamp_duration)):
        ranges_detail = {}
        ranges_detail['from'] = start_timestamp + i * timestamp_duration
        ranges_detail['to'] = start_timestamp + (i+1) * timestamp_duration
        ranges_detail['key'] = DateTimeUtil.timestamp_to_strtime((start_timestamp + i * timestamp_duration),'%Y-%m-%d %H' if time_key_type == 1 else '%Y-%m-%d')
        ranges.append(ranges_detail)

    return json.dumps(AppLog.get_range_general(start_timestamp, end_timstamp, ranges), ensure_ascii=False)

if __name__ == '__main__':
    start_time = '2018-11-18'
    end_time = '2018-11-20'
    context = "test"
    Mail.send(subject="正服接口返回异常", context=json_repot(start_time,end_time),to=['chao.song@maimob.cn'])



