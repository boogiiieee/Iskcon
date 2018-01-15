# -*- coding: utf-8 -*-

import os
import re
from django.http import Http404
from django.db.models import Q

from django_mailbox.models import Mailbox

from conference.models import Group


class MailboxPkPermissions(object):
    u"""
    Для файлов django_mailbox проверяем является ли пользователь участником 
    конференции, которой принадлежит этот mailbox.
    Для файлов сообщений конференций проверяем является ли пользователь 
    участником конференции.
    
    """
    def has_read_permission(self, request, path):
        user = request.user
        if not user.is_authenticated():
            return False
        elif user.is_superuser:
            return True
        elif user.is_staff:
            return True
        else:
            if re.findall(r'^upload/mailbox_attachments/', path):
                try:
                    mailbox_pk = int(os.path.split(os.path.split(path)[0])[1])
                except ValueError:
                    raise Http404('File not found')
                    
                for group in Group.objects.filter(Q(is_active=True) & (
                    Q(users=user) | Q(leaders=user)
                )):
                    if Mailbox.objects.filter(
                        id=mailbox_pk,
                        name=group.get_full_server_email(),
                        uri__contains=group.server_email_passw,
                    ).count():
                        return True
                
            elif re.findall(r'^upload/conference/message/', path):
                try:
                    group_pk = int(os.path.split(os.path.split(path)[0])[1])
                except ValueError:
                    raise Http404('File not found')
                    
                if Group.objects.filter(Q(pk=group_pk) & Q(is_active=True) & (
                    Q(users=user) | Q(leaders=user)
                )).count():
                    return True
                    
            return False