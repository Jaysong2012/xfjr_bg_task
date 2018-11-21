# -*- coding:utf-8 -*-

from libraries.Mail import Mail
from libraries.Utils import Utils
from libraries.DateTimeUtil import DateTimeUtil
from models.es.AppLog import AppLog
from email.mime.text import MIMEText
import json
from libraries.Scheduler import Scheduler
import time,datetime

def date_repot(start_date,end_date,time_key_type=0):
    start_time = start_date +' 00:00:00'
    end_time = end_date +' 23:59:59'

    start_timestamp = DateTimeUtil.strtime_to_timestamp(start_time, '%Y-%m-%d %H:%M:%S')
    end_timstamp = DateTimeUtil.strtime_to_timestamp(end_time, '%Y-%m-%d %H:%M:%S')+1000
    timestamp_duration = (1000 * 60 * 60) if time_key_type == 1 else (1000 * 60 * 60 * 24)
    ranges = []

    for i in range(int((end_timstamp - start_timestamp) / timestamp_duration)):
        ranges_detail = {}
        ranges_detail['from'] = start_timestamp + i * timestamp_duration
        ranges_detail['to'] = start_timestamp + (i + 1) * timestamp_duration
        ranges_detail['key'] = DateTimeUtil.timestamp_to_strtime((start_timestamp + i * timestamp_duration),
                                                          '%Y-%m-%d %H' if time_key_type == 1 else '%Y-%m-%d')
        ranges.append(ranges_detail)

    return AppLog.get_range_general(start_timestamp, end_timstamp, ranges)

def day_report():
    day_timestamp_duration = 24 * 60 * 60 * 1000
    today_begin_timestamp = DateTimeUtil.get_current_day_begin_timestamp()
    #yestoday_begin_timestamp = today_begin_timestamp - day_timestamp_duration
    two_day_ago_begin_timestamp = today_begin_timestamp - (2 * day_timestamp_duration)

    ranges = []

    for i in range(int((today_begin_timestamp - two_day_ago_begin_timestamp) / day_timestamp_duration)):
        ranges_detail = {}
        ranges_detail['from'] = two_day_ago_begin_timestamp + i * day_timestamp_duration
        ranges_detail['to'] = two_day_ago_begin_timestamp + (i + 1) * day_timestamp_duration
        ranges_detail['key'] = DateTimeUtil.timestamp_to_strtime((two_day_ago_begin_timestamp + i * day_timestamp_duration),'%Y-%m-%d')
        ranges.append(ranges_detail)

    Utils.log(str(ranges))

    return AppLog.get_range_general(two_day_ago_begin_timestamp, today_begin_timestamp, ranges)

def hour_report():
    now_hour_begin_timestamp = DateTimeUtil.strtime_to_timestamp(
        DateTimeUtil.datetime_to_strtime(datetime.datetime.now(), "%Y-%m-%d %H:00:00"), "%Y-%m-%d %H:%M:%S")
    one_hour_ago_timestamp = DateTimeUtil.strtime_to_timestamp(
        DateTimeUtil.datetime_to_strtime(datetime.datetime.now() - datetime.timedelta(hours=1), "%Y-%m-%d %H:00:00"),
        "%Y-%m-%d %H:%M:%S")

    yestoday_hour_begin_timestamp = DateTimeUtil.strtime_to_timestamp(
        DateTimeUtil.datetime_to_strtime(datetime.datetime.now() - datetime.timedelta(days=1), "%Y-%m-%d %H:00:00"), "%Y-%m-%d %H:%M:%S")
    yestoday_hour_ago_timestamp = DateTimeUtil.strtime_to_timestamp(
        DateTimeUtil.datetime_to_strtime(datetime.datetime.now() - datetime.timedelta(days=1,hours=1), "%Y-%m-%d %H:00:00"),
        "%Y-%m-%d %H:%M:%S")

    print(now_hour_begin_timestamp,one_hour_ago_timestamp,yestoday_hour_begin_timestamp,yestoday_hour_ago_timestamp)
    timestamp_duration = (1000 * 60 * 60)
    ranges = []

    for i in range(int((now_hour_begin_timestamp - one_hour_ago_timestamp) / timestamp_duration)):
        ranges_detail = {}
        ranges_detail['from'] = one_hour_ago_timestamp + i * timestamp_duration
        ranges_detail['to'] = one_hour_ago_timestamp + (i + 1) * timestamp_duration
        ranges_detail['key'] = DateTimeUtil.timestamp_to_strtime((one_hour_ago_timestamp + i * timestamp_duration),'%Y-%m-%d %H')
        ranges.append(ranges_detail)

    for i in range(int((yestoday_hour_begin_timestamp - yestoday_hour_ago_timestamp) / timestamp_duration)):
        ranges_detail = {}
        ranges_detail['from'] = yestoday_hour_ago_timestamp + i * timestamp_duration
        ranges_detail['to'] = yestoday_hour_ago_timestamp + (i + 1) * timestamp_duration
        ranges_detail['key'] = DateTimeUtil.timestamp_to_strtime((yestoday_hour_ago_timestamp + i * timestamp_duration),'%Y-%m-%d %H')
        ranges.append(ranges_detail)

    print(ranges)

    should = [
                        {
                            "range":
                                {
                                    "request.baseRequest.timeStamp": {
                                        "gte": yestoday_hour_ago_timestamp,
                                        "lte": yestoday_hour_begin_timestamp
                                    }
                                }
                        },
                        {
                            "range":
                                {
                                    "request.baseRequest.timeStamp": {
                                        "gte": one_hour_ago_timestamp,
                                        "lte": now_hour_begin_timestamp
                                    }
                                }
                        }
                    ]

    print(should)

    return AppLog.should_range_general(should,ranges)

def html_report(time_key_report_list,title):
    html_start = '''
<html>
    <body>
    '''
    html_title = '    	<h1><pre>'+title+'</pre></h1>'
    html_table = '''
    	<div class="data">
        	<table style="width:100%;" border=1 cellspacing=0>
        		<tr>
        			<td style="width:10%;">时间</td>
        			<td style="width:10%;">总调用数量</td>
        			<td style="width:24%;">接口</td>
        			<td style="width:8%;">调用次数</td>
        			<td style="width:10%;">返回码</td>
        			<td style="width:30%;">错误信息</td>
        			<td style="width:8%;">返回次数</td>
        		</tr>
        	</table>
            <table style="width:100%;" border=1 cellspacing=0>
            	<tr>
            		<td style="width:10%;"></td>
            		<td style="width:10%;"></td>
            		<td style="width:80%;"></td>
            	</tr>
        '''
    html_body = ''
    for l in time_key_report_list:
        html_body += '        		<tr>'
        html_body += '        			<td style="width:10%;">' + l['time_key'] + '</td>\n'
        html_body += '                    <td style="width:10%;">' + str(l['doc_count']) + '</td>\n'
        html_body += '                    <td style="width:80%;">\n'
        html_body += '                    	<table style="width:100%;" border=1 cellspacing=0>\n'

        for call in l['call_stat']:
            html_body += '        					<tr>\n'
            html_body += '        						<td style="width:30%;">' + call['call'] + '</td>\n'
            html_body += '        						<td style="width:10%;">' + str(call['call_num']) + '</td>\n'
            html_body += '        						<td style="width:60%;">\n'
            html_body += '        							<table style="width:100%;" border=1 cellspacing=0>\n'
            for return_stat in call['return_stat']:
                html_body += '        								<tr>\n'
                html_body += '        									<td style="width:20%;">' + return_stat[
                    'return_code'] + '</td>\n'
                html_body += '        									<td style="width:60%;">' + return_stat[
                    'return_msg'] + '</td>\n'
                html_body += '        									<td style="width:20%;">' + return_stat[
                    'return_num'] + '</td>\n'
                html_body += '        								</tr>\n'
            html_body += '        							</table >\n'
            html_body += '        						</td>\n'
            html_body += '        					</tr>\n'

        html_body += '                    	</table>\n'
        html_body += '                    </td>\n'
        html_body += '        		</tr>'

    html_end = '''
            </table>
    	</div>
    </body>
</html>
        '''
    return html_start+html_title+html_table+html_body+html_end

def send_day_report():
    Utils.log('六合一每天报告开始')
    Mail.html_send(subject="六合一每天API调用概览", msg=MIMEText(html_report(day_report(),"六合一每天API调用概览"),
                                                      _subtype='html',  _charset='utf-8'),to=['xfjr_server@maimob.cn'])
    Utils.log('六合一每天邮件发送成功')

def send_hour_report():
    report = hour_report()
    call_detail_yestoday = report[0]
    call_detail_today = report[1]
    Utils.log(call_detail_today['time_key'] + '报告准备发送')
    title = '六合一API'+call_detail_today['time_key']+'调用概览\n'
    for call_stat_today in call_detail_today['call_stat']:
        call = call_stat_today['call']
        call_num = call_stat_today['call_num']
        succeed_rate = call_stat_today.get('succeed_rate',0)
        yestoday_same_call = get_yestoday_same_call(call,call_detail_yestoday)

        if yestoday_same_call is not None:
            print(yestoday_same_call)
            if call_num == 0 :
                title += str(call) + ' 接口调用数量异常今日单小时 ' + str(call_num) + ' 昨日单小时 ' + str(yestoday_same_call['call_num']) + '\n'
            elif yestoday_same_call.get('call_num',0) != 0 and int(abs(call_num - yestoday_same_call['call_num']) * 100 / call_num) > 30 and (call_num - yestoday_same_call['call_num'])<0:
                title +=str(call)+' 接口调用数量异常今日单小时 '+str(call_num)+' 昨日单小时 '+str(yestoday_same_call['call_num'])+'\n'

            if succeed_rate == 0:
                title += str(call) + ' 接口调用通过率异常今日单小时调用成功率 ' + str(succeed_rate) + ' 昨日单小时调用成功率' + str(yestoday_same_call['succeed_rate']) + '\n'
            elif yestoday_same_call.get('succeed_rate','')!='' and int(abs(succeed_rate - yestoday_same_call['succeed_rate']) * 100 / succeed_rate) >10  and (succeed_rate - yestoday_same_call['succeed_rate'])<0:
                title += str(call)+' 接口调用通过率异常今日单小时调用成功率 '+str(succeed_rate)+' 昨日单小时调用成功率'+str(yestoday_same_call['succeed_rate'])+'\n'

    #
    Mail.html_send(subject='六合一API'+call_detail_today['time_key']+'调用概览', msg=MIMEText(html_report(report,title),
                                                      _subtype='html',  _charset='utf-8'),to=['chao.song@maimob.cn', 'feng.yang@maimob.cn', 'junpeng.guo@maimob.cn'])
    Utils.log(call_detail_today['time_key']+'邮件发送成功')


def get_yestoday_same_call(call,call_detail_yestoday):
    for call_stat_yestoday in call_detail_yestoday['call_stat']:
        if call_stat_yestoday['call'] == call:
            return call_stat_yestoday



def test_job():
    Utils.log('heart beat')

if __name__ == '__main__':
    # 挂载任务
    Utils.log('start')
    #print(json.dumps(hour_report(), ensure_ascii=False))
    scheduler = Scheduler.get_sched()
    #send_hour_report()
    scheduler.add_job(func=send_day_report, trigger='cron',hour=2,minute=18)
    scheduler.add_job(func=test_job, trigger='interval', minutes=1)
    scheduler.add_job(func=send_hour_report, trigger='interval', hours=1)
    scheduler.start()

    while True:
        time.sleep(10)

