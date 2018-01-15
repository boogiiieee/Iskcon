# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import datetime
import re, os

from pytils.translit import slugify
from sorl.thumbnail import ImageField as SorlImageField
from redactor.fields import RedactorField
from engine.models import make_file_path, MetaModel, ActiveSortModel, DateCreateModel

##########################################################################
##########################################################################

class PublicManager(models.Manager): 
	def get_query_set(self): 
		return super(PublicManager, self).get_query_set().filter(is_active=True, is_public = True)

class NewsArticle(MetaModel, ActiveSortModel, DateCreateModel):
	def make_upload_path(instance, filename):
		return make_file_path(filename, u'upload/news/')
		
	title = models.CharField(max_length=100, verbose_name=u'заголовок')
	image = SorlImageField(max_length=100, upload_to=make_upload_path, verbose_name=u'изображение', help_text=u'рекомендованный размер изображения - 350px*200px')
	announcement = models.TextField(max_length=1000, verbose_name=u'краткое описание')
	text = RedactorField(max_length=100000, verbose_name=u'полное описание')
	
	is_public = models.BooleanField(verbose_name=u'является публичной', default=False)
	
	objects = models.Manager()	
	publics = PublicManager()
	
	def get_title(self): return self.title
	def get_image(self): return self.image
	def get_announcement(self): return self.announcement
	def get_text(self): return self.text
	def get_comment_count(self): return self.text
	
	def __unicode__(self):
		return self.get_title()

	@models.permalink
	def get_absolute_url(self):
		return ('news_item_url', (), {'id': self.id})
		
	class Meta: 
		verbose_name = u'новость'
		verbose_name_plural = u'новости'
		ordering = ['sort', '-created']
		
##########################################################################
##########################################################################