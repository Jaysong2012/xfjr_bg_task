# -*- coding: utf-8 -*-
import time
from datetime import datetime
class DateTimeUtil:
    @staticmethod
    def timestamp_to_strtime(timestamp,str_format='%Y-%m-%d %H:%M:%S.%f'):
        """秒/毫秒时间戳转化成本地普通时间 (字符串格式)
        :param timestamp: 10／13 位整数的时间戳 (1542623780／1456402864242)
        :param str_format: 返回字符串格式 默认 %Y-%m-%d %H:%M:%S.%f
        :return: 返回字符串格式 {str}'2016-02-25 20:21:04.242000'
        """
        return datetime.fromtimestamp((timestamp / 1000.0) if len(str(timestamp)) == 13 else timestamp).strftime(str_format)

    @staticmethod
    def timestamp_to_datetime(timestamp):
        """将 10/13 位整数的毫秒时间戳转化成本地普通时间 (datetime 格式)
        :param timestamp: 10/13 位整数的毫秒时间戳 (1456402864242)
        :return: 返回 datetime 格式 {datetime}2016-02-25 20:21:04.242000
        """
        return datetime.fromtimestamp((timestamp / 1000.0) if len(str(timestamp)) == 13 else timestamp)

    @staticmethod
    def datetime_to_strtime(datetime_obj, str_format="%Y-%m-%d %H:%M:%S.%f"):
        """将 datetime 格式的时间 (含毫秒) 转为字符串格式
        :param datetime_obj: {datetime}2016-02-25 20:21:04.242000
        :param str_format: 返回字符串格式 默认 %Y-%m-%d %H:%M:%S.%f
        :return: {str}'2016-02-25 20:21:04.242'
        """
        return datetime_obj.strftime(str_format)

    @staticmethod
    def datetime_to_timestamp(datetime_obj):
        """将本地(local) datetime 格式的时间 (含毫秒) 转为毫秒时间戳
        :param datetime_obj: {datetime}2016-02-25 20:21:04.242000
        :return: 13 位的毫秒时间戳  1456402864242
        """
        return int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)

    @staticmethod
    def strtime_to_datetime(timestr,str_fromat="%Y-%m-%d %H:%M:%S.%f"):
        """将字符串格式的时间 (含毫秒) 转为 datetiem 格式
        :param timestr: {str}'2016-02-25 20:21:04.242'
        :param str_format: 返回字符串格式 默认 %Y-%m-%d %H:%M:%S.%f
        :return: {datetime}2016-02-25 20:21:04.242000
        """
        return datetime.strptime(timestr, str_fromat)

    @classmethod
    def strtime_to_timestamp(cls,local_timestr,str_fromat="%Y-%m-%d %H:%M:%S.%f"):
        """将本地时间 (字符串格式，含毫秒) 转为 13 位整数的毫秒时间戳
        :param local_timestr: {str}'2016-02-25 20:21:04.242'
        :param str_format: 返回字符串格式 默认 %Y-%m-%d %H:%M:%S.%f
        :return: 1456402864242
        """
        return cls.datetime_to_timestamp(cls.strtime_to_datetime(local_timestr,str_fromat))


if __name__ == '__main__':
    # 当前时间：datetime 格式
    print(datetime.now())
    # 当前时间：字符串格式
    print(DateTimeUtil.datetime_to_strtime(datetime.now()))
    # 当前时间：时间戳格式 13位整数
    print(DateTimeUtil.datetime_to_timestamp(datetime.now()))

    print(DateTimeUtil.timestamp_to_strtime(1542623780,'%Y-%m-%d %H:%M:%S'))
    print(DateTimeUtil.timestamp_to_strtime(1456402864242))
    print(DateTimeUtil.timestamp_to_datetime(1542623780))
    print(DateTimeUtil.timestamp_to_datetime(1456402864242))

    print(DateTimeUtil.datetime_to_strtime(datetime.now()))

    print(DateTimeUtil.strtime_to_timestamp('2018-11-20 00:00:00.000'))
    print(DateTimeUtil.strtime_to_timestamp('2018-11-20', '%Y-%m-%d'))
    print(DateTimeUtil.strtime_to_timestamp('2018-11-21', '%Y-%m-%d'))
    print(DateTimeUtil.strtime_to_timestamp('2018-11-20 00:00:00', '%Y-%m-%d %H:%M:%S'))