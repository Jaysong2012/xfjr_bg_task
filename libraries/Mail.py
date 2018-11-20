# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
class Mail:
    # 用户信息
    # from_addr = 'ting.wang@maimob.cn'
    # password = '*******'
    # 腾讯服务器地址
    # smtp_server = 'smtp.exmail.qq.com'
    # 阿里云邮箱
    # smtp_server = 'smtp.mxhichina.com'
    @staticmethod
    def send(subject,context,to,user='loan.admin@maimob.cn', password='Maimob2016Admin', smtp_server = 'smtp.exmail.qq.com'):
        #  内容初始化，定义内容格式（普通文本，html）
        msg = MIMEText(context, 'plain', 'utf-8')
        # 发件人收件人信息格式化 ，可防空
        #  固定用法不必纠结，使用lambda表达式进行简单封装方便调用
        lam_format_addr = lambda name, addr: formataddr((Header(name, 'utf-8').encode(), addr))
        msg['From'] = lam_format_addr('WarningAdmin', user)
        # msg['To'] = lam_format_addr('收件人昵称（服务商会自动替换成用户名）', to_addr)
        #  邮件标题
        msg['Subject'] = Header(subject, 'utf-8').encode()  # 腾讯邮箱略过会导致邮件被屏蔽
        #  服务端配置
        # server = smtplib.SMTP(smtp_server, 25)
        # 腾讯邮箱支持SSL(不强制)， 不支持TLS。
        server = smtplib.SMTP_SSL(smtp_server, 465) # 按需开启
        #  调试模式，打印日志 # server.set_debuglevel(1) # 按需开启
        #  登陆服务器
        server.login(user, password)
        try:
            server.sendmail(user, to, msg.as_string())
            server.quit()
        except Exception as e:
            #('/tmp/mail.log', "发送邮件失败" + str(e))
            print("发送邮件失败" + str(e))

    @staticmethod
    def html_send(subject,msg,to,user='loan.admin@maimob.cn', password='Maimob2016Admin', smtp_server = 'smtp.exmail.qq.com'):
        lam_format_addr = lambda name, addr: formataddr((Header(name, 'utf-8').encode(), addr))
        msg['From'] = lam_format_addr('WarningAdmin', user)
        # msg['To'] = lam_format_addr('收件人昵称（服务商会自动替换成用户名）', to_addr)
        #  邮件标题
        msg['Subject'] = Header(subject, 'utf-8').encode()  # 腾讯邮箱略过会导致邮件被屏蔽
        #  服务端配置
        # server = smtplib.SMTP(smtp_server, 25)
        # 腾讯邮箱支持SSL(不强制)， 不支持TLS。
        server = smtplib.SMTP_SSL(smtp_server, 465) # 按需开启
        #  调试模式，打印日志 # server.set_debuglevel(1) # 按需开启
        #  登陆服务器
        server.login(user, password)
        try:
            server.sendmail(user, to, msg.as_string())
            server.quit()
        except Exception as e:
            #('/tmp/mail.log', "发送邮件失败" + str(e))
            print("发送邮件失败" + str(e))
