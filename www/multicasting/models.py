# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from redactor.fields import RedactorField

from engine.models import make_file_path, ActiveSortModel, DateCreateModel
from pytils.translit import slugify
import os

################################################################################################################
################################################################################################################
class GroupPermMulticasting(ActiveSortModel):
	title = models.CharField(max_length=500, verbose_name=u'заголовок')

	user = models.ManyToManyField(User, verbose_name=u'пользователи', blank=True, related_name = 'user_group_perm_rel', help_text=u'Пользователи могут писать только в пределах группы')
	leader = models.ManyToManyField(User, verbose_name=u'лидеры группы', blank=True, related_name = 'leader_group_perm_rel', help_text=u'Пользователи могут писать абсолютно всем')
	
	objects = models.Manager()	
		
	def get_title(self): return self.title
	
	def __unicode__(self):
		return self.get_title()
		
	@models.permalink
	def get_absolute_url(self):
		return ('group_perm_multicasting_url', (), {'id':self.id})
		
		
	class Meta: 
		verbose_name = u"группа прав пользователей"
		verbose_name_plural = u"группы прав пользователей"

#смс
class MessagesMulticasting(ActiveSortModel, DateCreateModel):
	def make_upload_path(instance, filename):
		name, extension = os.path.splitext(filename)
		filename = u'%s%s' % (slugify(name), extension)
		return u'upload/multicasting/%d/%s' % (instance.user.id, filename.lower())
		
	user = models.ForeignKey(User, verbose_name=u'пользователь', related_name='user_mes_rel')
	recipient = models.ManyToManyField(User, verbose_name=u'получатели смс', through="RecipientMulticasting", blank=True, null=True)
							   
	theme = models.CharField(max_length=500, verbose_name=u'тема сообщения')
	text = RedactorField(max_length=10000, verbose_name=u"текст сообщения")
	file = models.FileField(max_length=500, upload_to=make_upload_path, verbose_name=u'файл', blank=True)
	
	def __unicode__(self):
		return u'%s - %s' % (self.user, self.theme)
		
	def get_title(self): return self.theme
	def get_text(self): return self.text
	def get_file(self): return self.file
	
	def get_recipient(self):
		html = u''
		for i in self.recipient.all():
			html = html + u'%s, ' % i.get_full_name()
		return html
	
	@models.permalink
	def get_outbox_item_url(self):
		return ('outbox_item_multicasting_url', (), {'id':self.id})
	
	@models.permalink	
	def get_delete_url(self):
		return ('outbox_delete_multicasting_url', (), {'id':self.id})

	class Meta: 
		verbose_name = u'сообщение'
		verbose_name_plural = u'сообщения'
		ordering = ['-created', '-modified', '-id']
		
#Получатели смс
class RecipientMulticasting(ActiveSortModel, DateCreateModel):
	user = models.ForeignKey(User, verbose_name=u'пользователь', related_name='recipient_user_rel')
	sms = models.ForeignKey(MessagesMulticasting, verbose_name=u'сообщение', related_name='recipient_sms_rel')
	is_new = models.BooleanField(verbose_name=u'Новое сообщение', default=True)
	
	def get_title(self):return u'%s - %s' % (self.user, self.sms)
		
	def __unicode__(self):return self.get_title()
	
	def get_user(self):
		return self.sms.user.get_full_name()
		
	@models.permalink
	def get_inbox_item_url(self):
		return ('inbox_item_multicasting_url', (), {'id':self.id})
		
	@models.permalink	
	def get_delete_url(self):
		return ('inbox_delete_multicasting_url', (), {'id':self.id})

	
	class Meta: 
		verbose_name = u'получатель смс' 
		verbose_name_plural = u'получатели смс'
		ordering = ['-id',]
		
################################################################################################################
################################################################################################################