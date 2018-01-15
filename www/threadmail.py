# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import Context, loader
from django.core.mail import EmailMessage
from django.conf import settings
import threading
import logging

logger = logging.getLogger('threadmail')

###############################################################################
###############################################################################

def get_email(email, sender_name=None):
    u"""
    Возвращает адрес отправителя. Если задан sender_name, то подставляет
    псевдоним.
    
    """
    if sender_name:
        return u'%s <%s>' % (sender_name, email)
    return email

###############################################################################
###############################################################################

def simple_send_mail(template, head, addresses, params, from_email=None,
                     connection=None, sender_name=None, headers={}):
    u"""
    Отправляет HTML сообщение.
    addresses - список получателей.
    sender_name - псевдоним отправителя.
    headers - дополнительны заголовки.
    Например headers = {'To':'info@web-aspect.ru'}
    
    """    
    sender = from_email or settings.DEFAULT_FROM_EMAIL
    t = loader.get_template(template)
    body = t.render(Context(params))
    msg = EmailMessage(
        head, body, get_email(sender, sender_name), addresses,
        connection=connection, headers=headers
    )
    msg.content_subtype = "html"
    #msg.encoding = 'utf-8'
    msg.send(fail_silently=True)
        
    
def threading_simple_send_mail(template, head, addresses, params,
                               from_email=None, connection=None,
                               sender_name=None):
    t = threading.Thread(
        target=simple_send_mail,
        args=(template, head, addresses, params, from_email, connection,
              sender_name)
    )
    t.start()

###############################################################################
###############################################################################

def threading_send_mail(template, head, addresses, params):
    body = '%s' % render_to_response(template, params)._get_content()
    msg = EmailMessage(head, body, settings.DEFAULT_FROM_EMAIL, addresses)
    msg.content_subtype = "html"
    t = threading.Thread(target=msg.send)
    t.start()

###############################################################################
###############################################################################