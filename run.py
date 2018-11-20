# -*- coding:utf-8 -*-

from libraries.Mail import Mail
from libraries.Utils import Utils
from libraries.DateTimeUtil import DateTimeUtil
from models.es.AppLog import AppLog
from email.mime.text import MIMEText
import json
from libraries.Scheduler import Scheduler
import time,datetime

def json_repot(start_date,end_date,time_key_type=0):
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

    return json.dumps(AppLog.get_range_general(start_timestamp, end_timstamp, ranges), ensure_ascii=False)

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

    print(ranges)

    return AppLog.get_range_general(two_day_ago_begin_timestamp, today_begin_timestamp, ranges)

def send_day_report():
    time_key_report_list = day_report()
    html_start = '''
<html>
	<body>
		<h1>六合一API调用概览</h1>
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
        html_body +='        		<tr>'
        html_body += '        			<td style="width:10%;">' + l['time_key'] + '</td>\n'
        html_body += '                    <td style="width:10%;">' + str(l['doc_count']) + '</td>\n'
        html_body += '                    <td style="width:80%;">\n'
        html_body += '                    	<table style="width:100%;" border=1 cellspacing=0>\n'

        for call in l['call_stat']:
            html_body +='        					<tr>\n'
            html_body +='        						<td style="width:30%;">' + call['call'] + '</td>\n'
            html_body +='        						<td style="width:10%;">' + str(call['call_num']) + '</td>\n'
            html_body +='        						<td style="width:60%;">\n'
            html_body +='        							<table style="width:100%;" border=1 cellspacing=0>\n'
            for return_stat in call['return_stat']:
                html_body += '        								<tr>\n'
                html_body += '        									<td style="width:20%;">'+return_stat['return_code']+'</td>\n'
                html_body += '        									<td style="width:60%;">' + return_stat['return_msg'] + '</td>\n'
                html_body += '        									<td style="width:20%;">' + return_stat['return_num'] + '</td>\n'
                html_body += '        								</tr>\n'
            html_body +='        							</table >\n'
            html_body +='        						</td>\n'
            html_body +='        					</tr>\n'


        html_body += '                    	</table>\n'
        html_body += '                    </td>\n'
        html_body += '        		</tr>'

    html_end = '''
            </table>
		</div>
	</body>
</html>
    '''
    #print(json.dumps(time_key_report_list, ensure_ascii=False))
    Mail.html_send(subject="六合一API调用概览", msg=MIMEText((html_start+html_body+html_end), _subtype='html',  _charset='utf-8'),to=['xfjr_server@maimob.cn'])
    print('邮件发送成功')

def test_job():
    Utils.log(DateTimeUtil.datetime_to_strtime(datetime.datetime.now())+'heart beat')

if __name__ == '__main__':
    # 挂载任务
    Utils.log('start')
    scheduler = Scheduler.get_sched()
    #send_day_report()
    scheduler.add_job(func=send_day_report, trigger='cron',hour=2,minute=18)
    scheduler.add_job(func=test_job, trigger='interval', minutes=1)
    scheduler.start()

    while True:
        time.sleep(10)

