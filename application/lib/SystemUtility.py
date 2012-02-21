#!/usr/bin/env python
# -*- coding:utf-8 -*-

def putResponse(start_response, body):
    status = '200 OK'
    header = [('Content-Type', 'text/html; charset=UTF-8'),
              ('Content-Length', str(len(body)))]

    start_response(status, header)

def getRequest(environ):
    from cgi import parse_qs

    request_size = environ.get('CONTENT_LENGTH')
    if request_size:
        request_body = environ['wsgi.input'].read(int(request_size))
        post_info = parse_qs(request_body)
        return post_info

    return None

def convertString(target, replace, src):
    if (src == ''):
        return ''

    import re

    return re.sub(target, replace, str(src))

def createErrorTemplate():
    from Cheetah.Template import Template
    import traceback
    import sys
    import os

    template = Template(file='/develop/MailForm/application/mailform/template/error.tmpl')
    template.error_data = {}
    error_message = traceback.format_exc(sys.exc_info()[2])
    template.error_data['error_log'] = convertString('\n', '<br />', error_message)
