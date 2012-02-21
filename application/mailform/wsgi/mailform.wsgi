# -*- coding:utf-8 -*-

from Cheetah.Template import Template
import SystemUtility
import MailformModule

def application(environ, start_response):
    try:
        viewData = MailformModule.createMailformViewData(environ)

        if(viewData.navigation == ''):
            template = Template(
                file='/develop/MailForm/application/mailform/template/mailform.tmpl')
            template.viewData = viewData

        elif(viewData.navigation == '001'):
            template = Template(
                file='/develop/MailForm/application/mailform/template/mailform_check.tmpl')
            template.viewData = MailformModule.checkViewData(viewData)

        elif(viewData.navigation == '002'):
            template = Template(
                file='/develop/MailForm/application/mailform/template/mailform_send.tmpl')
            template.viewData = viewData
            # MailformModule.sendMail(viewData)

    except:
        template = SystemUtility.createErrorTemplate()

    body = template.respond().encode('utf-8')

    SystemUtility.putResponse(start_response, body)

    return [body]
