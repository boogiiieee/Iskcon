# -*- coding: utf-8 -*-

from django.db import models
import datetime
import re, os

from pytils.translit import slugify
from sorl.thumbnail import ImageField as SorlImageField
from redactor.fields import RedactorField

u'''
MetaModel,
ActiveModel, SortModel, ActiveSortModel,
DateCreateModel,
FileModelReq, FileModel, ImageModelReq, ImageModel,

TitleModel, Title1Model, Title2Model, Title3Model,
ArticleModel, Article1Model,
ArticleImageModel, ArticleImage1Model,
ArticleImageReqModel, ArticleImageReq1Model,
'''

##########################################################################
##########################################################################

def make_file_path(filename, path=u'upload/'):
	u'''Формирует имя файла и путь для загрузки файла'''
	name, extension = os.path.splitext(filename)
	filename = u'%s%s' % (slugify(name), extension)
	return u'%s%s' % (path, filename.lower())
	
##########################################################################
##########################################################################

##########################################################################
##########################################################################

class MetaModel(models.Model):
	u'''Абстрактный класс мета-тэгов'''
	meta_title = models.TextField(verbose_name=u'title', blank=True)
	meta_description = models.TextField(verbose_name=u'description', blank=True)
	meta_keywords = models.TextField(verbose_name=u'keywords', blank=True)
	
	class Meta:
		abstract = True
		
##########################################################################
##########################################################################

class ActiveManager(models.Manager): 
	def get_query_set(self): 
		return super(ActiveManager, self).get_query_set().filter(is_active=True)

class ActiveModel(models.Model):
	u'''Абстрактный класс активность'''
	is_active = models.BooleanField(verbose_name=u'активно', default=True)
	
	objects = models.Manager()
	activs = ActiveManager()
	
	class Meta:
		abstract = True
		
class SortModel(models.Model):
	u'''Абстрактный класс сортировка'''
	sort = models.IntegerField(verbose_name=u'сортировка', default=1)
	
	class Meta:
		abstract = True
		ordering = ['sort',]
		
class ActiveSortModel(ActiveModel, SortModel):
	u'''Абстрактный класс активность, сортировка'''
	class Meta(ActiveModel.Meta, SortModel.Meta):
		abstract = True

##########################################################################
##########################################################################

class DateCreateModel(models.Model):
	u'''Абстрактный класс дата создания/изменения'''
	created = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
	modified = models.DateTimeField(verbose_name=u'дата изменения', auto_now=True)
	
	def get_created(self): return self.created
	def get_modified(self): return self.modified	
	
	class Meta:
		abstract = True
		
##########################################################################
##########################################################################

class TextAnnouncementModelReq(models.Model):
	u'''Абстрактный класс обязательные краткое/полное описание'''
	announcement = models.TextField(max_length=1000, verbose_name=u'краткое описание')
	text = RedactorField(max_length=10000, verbose_name=u"полное описание")
	
	def get_announcement(self): return self.announcement
	def get_text(self): return self.text
	
	class Meta:
		abstract = True
		
##########################################################################
##########################################################################

class FileModelReq(models.Model):
	u'''Абстрактный класс обязательный файл'''
	
	def make_upload_path(instance, filename):
		name, extension = os.path.splitext(filename)
		filename = u'%s%s' % (slugify(name), extension)
		return u'upload/file/%s' % filename.lower()
		
	file = models.FileField(max_length=500, upload_to=make_upload_path, verbose_name=u'файл')
	
	class Meta:
		abstract = True
		
class FileModel(models.Model):
	u'''Абстрактный класс файл'''
	
	def make_upload_path(instance, filename):
		name, extension = os.path.splitext(filename)
		filename = u'%s%s' % (slugify(name), extension)
		return u'upload/file/%s' % filename.lower()
		
	file = models.FileField(max_length=500, upload_to=make_upload_path, verbose_name=u'файл', blank=True, null=True)
	
	class Meta:
		abstract = True
		
##########################################################################
##########################################################################

class ImageModelReq(models.Model):
	u'''Абстрактный класс обязательный файл'''
	
	def make_upload_path(instance, filename):
		name, extension = os.path.splitext(filename)
		filename = u'%s%s' % (slugify(name), extension)
		return u'upload/image/%s' % filename.lower()
		
	image = SorlImageField(max_length=500, upload_to=make_upload_path, verbose_name=u'изображение')
	
	class Meta:
		abstract = True
		
class ImageModel(models.Model):
	u'''Абстрактный класс файл'''
	
	def make_upload_path(instance, filename):
		name, extension = os.path.splitext(filename)
		filename = u'%s%s' % (slugify(name), extension)
		return u'upload/image/%s' % filename.lower()
		
	image = SorlImageField(max_length=500, upload_to=make_upload_path, verbose_name=u'изображение', blank=True, null=True)
	
	class Meta:
		abstract = True
		
##########################################################################
##########################################################################

##########################################################################
##########################################################################

class TitleModel(models.Model):
	u'''Абстрактный класс только заголовок'''
	title = models.CharField(max_length=500, verbose_name=u'заголовок')
	
	def get_title(self):
		return self.title
	
	class Meta:
		abstract = True
		ordering = ['title']
		
class Title1Model(TitleModel, ActiveSortModel):
	u'''Абстрактный класс только заголовок + активность, сортировка'''
	class Meta(TitleModel.Meta, ActiveSortModel.Meta):
		abstract = True
		ordering = ['sort', 'title']
		
class Title2Model(TitleModel, ActiveSortModel, DateCreateModel):
	u'''Абстрактный класс только заголовок + активность, сортировка + дата создания/изменения'''
	class Meta(TitleModel.Meta, ActiveSortModel.Meta, DateCreateModel.Meta):
		abstract = True
		ordering = ['sort', '-created', 'title']
		
class Title3Model(TitleModel, ActiveSortModel, DateCreateModel, MetaModel):
	u'''Абстрактный класс только заголовок + активность, сортировка + дата создания/изменения + мета-теги'''
	class Meta(TitleModel.Meta, ActiveSortModel.Meta, DateCreateModel.Meta, MetaModel.Meta):
		abstract = True
		ordering = ['sort', '-created', 'title']
		
##########################################################################
##########################################################################

class ArticleModel(models.Model):
	u'''Абстрактный класс статьи'''
	title = models.CharField(max_length=500, verbose_name=u'заголовок')
	text = RedactorField(max_length=100000, verbose_name=u'текст')
	
	def get_title(self):
		return self.title
		
	def get_text(self):
		return self.text
	
	class Meta:
		abstract = True
		ordering = ['title']
		
class Article1Model(ArticleModel, ActiveSortModel, DateCreateModel, MetaModel):
	u'''Абстрактный класс статьи + активность, сортировка + дата создания/изменения + мета-теги'''
	class Meta(ArticleModel.Meta, ActiveSortModel.Meta, DateCreateModel.Meta, MetaModel.Meta):
		abstract = True
		ordering = ['sort', '-created', 'title']
		

##########################################################################
##########################################################################

class ArticleImageModel(ImageModel, ArticleModel):
	u'''Абстрактный класс изображение + статьи'''
	class Meta(ImageModel.Meta, ArticleModel.Meta):
		abstract = True
		
class ArticleImage1Model(ImageModel, Article1Model):
	u'''Абстрактный класс изображение + статьи + активность, сортировка + дата создания/изменения + мета-теги'''
	class Meta(ImageModel.Meta, Article1Model.Meta):
		abstract = True
		
class ArticleImageReqModel(ImageModelReq, ArticleModel):
	u'''Абстрактный класс обязат. изображение + статьи'''
	class Meta(ImageModelReq.Meta, ArticleModel.Meta):
		abstract = True
		
class ArticleImageReq1Model(ImageModelReq, Article1Model):
	u'''Абстрактный класс обязат. изображение + статьи + активность, сортировка + дата создания/изменения + мета-теги'''
	class Meta(ImageModelReq.Meta, Article1Model.Meta):
		abstract = True

##########################################################################
##########################################################################

##########################################################################
##########################################################################