# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.contrib.sites.models import Site
from django.conf import settings

from threadmail import simple_send_mail
from configuration.views import get_config

from conference.models import ConferenceProfile, Message, MessageRecipientRel

###############################################################################
###############################################################################

class Command(NoArgsCommand):
	help = u"Отправить сообщения на почту пользователя. Все письма в одном "\
           u"письме."

	def handle_noargs(self, **options):
		domain = Site.objects.get_current().domain
		config = get_config()

		for profile in ConferenceProfile.objects.filter(
            dub_email=True, one_email=True
        ):
			messages = Message.objects.filter(
                message_recipient_rel__user=profile.user,
                message_recipient_rel__is_sent_email=False, is_moderate=True
            ).distinct().order_by('group', '-id')
			if messages:
				user = profile.user
				if user.email:
					simple_send_mail(
                        'mail/conference_send_one_email.html',
                        u'Новые сообщения на сайте %s' % domain,
                        [user.email],
                        {
                            'messages':messages, 'user':user, 'domain':domain,
                            'sign':config.get_email_sign()
                        }
                    )
				MessageRecipientRel.objects.filter(
                    message__in=messages, user=user
                ).update(is_sent_email=True)

###############################################################################
###############################################################################