# -*- coding: utf-8 -*-

from django.db import models
from django.utils.html import mark_safe

from redactor.fields import RedactorField
from sorl.thumbnail import ImageField as SorlImageField

from engine.models import make_file_path

#######################################################################################################################
#######################################################################################################################

#Настройки
class ConfigModel(models.Model):
	def make_upload_path(instance, filename):
		return make_file_path(filename, u'upload/config/')
		
	site_name = models.CharField(max_length=300, verbose_name=u"название сайта")	
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	image = SorlImageField(max_length=500, upload_to=make_upload_path, verbose_name=u'изображение', help_text=u'рекомендованный размер изображения - 1170px*300px')
	
	email_sign = RedactorField(max_length=1000, verbose_name=u'подпись в письме', blank=True, allow_file_upload=False, allow_image_upload=False)
	
	def get_site_name(self):return self.site_name
	def get_image(self):return self.image
	
	def get_email_sign(self):
		return mark_safe(self.email_sign)
	
	def __unicode__(self):
		return u'Настройки сайта'
		
	class Meta: 
		verbose_name = u'настройки' 
		verbose_name_plural = u'настройки'

#######################################################################################################################
#######################################################################################################################