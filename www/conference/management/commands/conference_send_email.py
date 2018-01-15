# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.contrib.sites.models import Site

from threadmail import get_email, simple_send_mail

from conference.models import MessageRecipientRel
from conference.conf import *

###############################################################################
###############################################################################

class Command(NoArgsCommand):
    help = u"Отправить сообщения на почту пользователя. Каждое сообщение в "\
           u"отдельном письме."

    def handle_noargs(self, **options):
        domain = Site.objects.get_current().domain
        
        for message in MessageRecipientRel.objects.filter(
            user__conference_profile__dub_email=True,
            user__conference_profile__one_email=False,
            message__is_moderate=True, is_sent_email=False
        ).distinct():
            to_user = message.user
            from_user = message.message.user
            group = message.message.group
            
            if to_user.email:
                email_data = group.get_email_data()
                server_email = get_email(
                    email_data['from_email'],
                    group.get_title()
                )
                
                if group.is_behalf_author and from_user.email:
                    #От имени автора сообщения
                    from_email = get_email(
                        from_user.email,
                        from_user.get_full_name() or from_user.username
                    )
                    to_email = to_user.email
                    headers = {'To':server_email}
                else:
                    #От имени группы
                    from_email = server_email
                    to_email = get_email(
                        to_user.email,
                        to_user.get_full_name() or to_user.username
                    )
                    headers = {}
                    
                simple_send_mail(
                    'mail/conference_send_email.html',
                    message.message.get_theme(),
                    [to_email,],
                    {
                        'message':message.message, 'group':group,
                        'domain':domain, 'sign':email_data['sign']
                    },
                    from_email = from_email,
                    headers = headers,
                )
                message.is_sent_email = True
                message.save()

###############################################################################
###############################################################################