# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
import datetime
import re

from threadmail import simple_send_mail
from django_mailbox.models import Message as MessageMailbox, MessageAttachment

from conference.models import Group, Message, MessageFile, MessageRecipientRel
from conference.conf import *


class Command(NoArgsCommand):
    help = "Забирает письма с почтового ящика."

    def handle_noargs(self, **options):
        domain = Site.objects.get_current().domain
        
        mail_box_list = [MAIL_LOGIN]
        for group in Group.activs.exclude(server_email_login=u''):
            mail_box_list.append(group.get_server_email_login())
        
        for box in mail_box_list:
            msg_list = MessageMailbox.incoming_messages.filter(
                mailbox__active=True, to_header__icontains=box, read=None
            ).distinct()
            
            def create_msg(group, user, msg, is_moderate):
                u"""
                Создает новое сообщение в группе.
                
                """
                
                if msg.html:
                    body = msg.html
                elif msg.text:
                    body = msg.text.replace(u'\n', u'<br>')
                else:
                    body = u''
                    
                attachment_list = MessageAttachment.objects.filter(message=msg)
                
                
                def replace_cid(s):
                    u"""
                    Заменяет cid изображения в html письма на url изображения.
                    На вход подается подстрока "cid:..."
                    
                    """
                    if u'"cid:' in s:
                        s = s[5:-1]
                    attachment = attachment_list.filter(headers__icontains=s)
                    if attachment:
                        attachment = attachment[0]
                        return u''.join([
                            settings.PROTOKOL,
                            domain,
                            attachment.document.url,
                        ])
                    return u''
                    
                body = re.sub('"cid:.+?"', lambda m: replace_cid(m.group()),
                              body)
                
                #Создаем сообщение
                instance = Message.objects.create(
                    group=group, user=user, theme=msg.subject, text=body,
                    is_moderate=is_moderate
                )
                
                #Прикрепляем файлы
                obj_list = []
                for a in attachment_list.exclude(
                    headers__icontains=u'Content-ID:'
                ):
                    obj_list.append(
                        MessageFile(message=instance, file=a.document)
                    )
                if obj_list:
                    MessageFile.objects.bulk_create(obj_list)
                
                #Рассылаем уведомления
                obj_list = []
                for u in group.get_recipient_list():
                    obj_list.append(
                        MessageRecipientRel(user=u, message=instance)
                    )
                if obj_list:
                    MessageRecipientRel.objects.bulk_create(obj_list)

            
            for item in msg_list:
                item.read=datetime.datetime.now()
                item.save()
                
                from_user_list = User.objects.filter(
                    email__in=item.from_address
                )
                group_list = Group.activs.filter(
                    server_email_login__in=item.to_addresses
                )
                
                for obj in group_list:
                    email_data = obj.get_email_data()

                    for user in from_user_list:
                        is_moderate = not obj.is_moderate
                        if obj.is_staff(user):
                            is_moderate = True
                        
                        if obj.is_in_group(user):
                            #Отправитель подписан на конференцию.
                            if not obj.is_banned(user) and\
                                    obj.can_write_message(user):
                                create_msg(obj, user, item, is_moderate)
                            else:
                                simple_send_mail(
                                    'mail/conference_failure.html',
                                    u'Отказано в публикации сообщения',
                                    [user.email],
                                    {'message':u'Причина отказа: У Вас нет '
                                     u'прав писать в конференции '
                                     u'"%s".' % obj.get_title(),
                                     'domain':domain,
                                     'sign':email_data['sign']},
                                    from_email = email_data['from_email'],
                                    sender_name = obj.get_title(),
                                )
                        
                        else:
                            #Отправитель не подписан на конференцию.
                            if obj.is_moderate and\
                                    obj.is_moderate_unregistered:
                                create_msg(obj, user, item, is_moderate)
                            else:
                                simple_send_mail(
                                    'mail/conference_failure.html',
                                    u'Отказано в публикации сообщения',
                                    [user.email],
                                    {u'message':u'Причина отказа: Вы не '
                                     u'подписаны на конференцию '
                                     u'"%s".' % obj.get_title(),
                                     'domain':domain,
                                     'sign':email_data['sign']},
                                    from_email = email_data['from_email'],
                                    sender_name = obj.get_title(),
                                )