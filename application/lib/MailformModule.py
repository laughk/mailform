#!/usr/bin/env python
# -*- coding:utf-8 -*-

import SystemUtility
from cgi import escape
import os

class MailformViewData:
    def __init__(self):
        self.navigation           = ''
        self.name               = ''
        self.mailaddress        = ''
        self.subject            = ''
        self.question           = ''

        self.sendbutton_visible = False

def createMailformViewData(environ):
    viewData = MailformViewData()
    post_info = SystemUtility.getRequest(environ)

    if (post_info):
        viewData.navigation     = post_info.get('navigation', [''])[0]
        viewData.name         = escape(post_info.get('name', [''])[0])
        viewData.mailaddress  = escape(post_info.get('mailaddress', [''])[0])
        viewData.subject      = escape(post_info.get('subject', [''])[0])
        viewData.question     = escape(SystemUtility.convertString('<br />',
                                            os.linesep,
                                            post_info.get('question', [''])[0]))

    return viewData

def checkViewData(viewData):

    if(len(viewData.name) == 0):
        viewData.name_error = '未入力です'
    elif(len(viewData.name.decode('utf-8')) > 20):
        viewData.name_error = '20文字以内で入力してください'
    else:
        viewData.name_error = ''

    if(len(viewData.mailaddress) == 0):
        viewData.mailaddress_error = '未入力です'
    elif(len(viewData.mailaddress.decode('utf-8')) > 50):
        viewData.mailaddress_error = '50文字以内で入力してください'
    elif("@" not in viewData.mailaddress):
        viewData.mailaddress_error = 'メールアドレスが正しくありません'
    else:
        viewData.mailaddress_error = ''

    if(len(viewData.subject) == 0):
        viewData.subject_error = '未入力です'
    elif(len(viewData.subject) > 20):
        viewData.subject_error = '20文字以内で入力してください。'
    else:
        viewData.subject_error =''

    if(len(viewData.question) == 0):
        viewData.question_error = '未入力です'
    elif(len(viewData.question.decode('utf-8')) > 300):
        viewData.question_error = '300文字以内で入力してください'
    else:
        viewData.question = SystemUtility.convertString(os.linesep, '<br />', viewData.question)
        viewData.question_error = ''

    if(viewData.name_error == '' and
        viewData.mailaddress_error == '' and
        viewData.question_error == ''):

        viewData.sendbutton_visible = True

    return viewData

def sendMail(viewData):
    import smtplib
    from email.MIMEText import MIMEText
    from email.Header import Header
    from email.Utils import formatdate
    import xml.sax.saxutils

    from_address = 'xxxx@xxxxx.xxx'
    to_address = 'xxxx@xxxxx.xxx'
    charset = 'ISO-2022-JP'
    subject = u'お問い合わせ'

    body = ''
    body  += "【名前】\n"
    body  += xml.sax.saxutils.unescape(viewData.name, {'&quot;':'"',})  + "\n"
    body  += "【メールアドレス】\n"
    body  += xml.sax.saxutils.unescape(viewData.mailaddress, {'&quot;':'"',})  + "\n"
    body  += "【件名】\n"
    body  += xml.sax.saxutils.unescape(viewData.subject, {'&quot;':'"',})  + "\n"
    body  += "【内容】\n"
    body  += xml.sax.saxutils.unescape(viewData.question, {'&quot;':'"',})  + "\n"

    msg = MIMEText(body.encode(charset), "plain", charset)
    msg['Subject']    = Header(subject, charset)
    msg['From']       = from_address
    msg['To']         = to_address
    msg['Date']       = formatdate(localtime=True)

    smtp = smtplib.SMTP('xxxxxx.xx.jp')
    smtp.sendmail(from_address, to_address, msg.as_string())
    smtp.close()
