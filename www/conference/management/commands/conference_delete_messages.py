# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
import datetime

from conference.models import Message

#######################################################################################################################
#######################################################################################################################

class Command(NoArgsCommand):
	help = "Удаляет сообщения в группах, у которых установленно время жизни сообщений"

	def handle_noargs(self, **options):		
		for i in Message.objects.filter(group__lifetime__gt=0):
			if datetime.datetime.now() > ( i.created + datetime.timedelta(days=i.group.lifetime) ):
				i.delete()

#######################################################################################################################
#######################################################################################################################