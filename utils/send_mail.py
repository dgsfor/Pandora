# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from .secret import EMAILSEC

def SendEmail(receiver_list,subject,content):
    sender = EMAILSEC["EMAIL_SENDER"]
    subject = subject
    smtpserver = EMAILSEC["EMAIL_SMTP_SERVER"]
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = formataddr((str(Header('【Alert】XX运维告警系统', 'utf-8')), sender))
    msg['Subject'] = Header(subject, 'utf-8')
    msg['To'] = receiver_list  # 字符串
    smtp = smtplib.SMTP_SSL(smtpserver)
    smtp.login(EMAILSEC["EMAIL_USER"], EMAILSEC["EMAIL_PASSWORD"])
    smtp.sendmail(sender,receiver_list.split(','), msg.as_string())
    smtp.quit()