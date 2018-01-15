# -*- coding: utf-8 -*-

from django.db import models

from sorl.thumbnail import ImageField as SorlImageField
from sorl.thumbnail.shortcuts import get_thumbnail, delete

try: import Image
except ImportError:
	try: from PIL import Image
	except ImportError: raise ImportError("The Python Imaging Library was not found.")

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from redactor.fields import RedactorField	
from engine.models import make_file_path, MetaModel, ActiveSortModel, DateCreateModel, TextAnnouncementModelReq

################################################################################################################
################################################################################################################

class PublicManager(models.Manager): 
	def get_query_set(self): 
		return super(PublicManager, self).get_query_set().filter(is_active=True, is_public = True)

class CategoryArticle(MPTTModel, MetaModel, ActiveSortModel):
	parent = TreeForeignKey('self', verbose_name=u"родительская категория", blank=True, null=True, related_name='children_category')
	title = models.CharField(max_length=100, verbose_name=u'заголовок')
	text = RedactorField(max_length=1000, verbose_name=u"описание")
	
	is_public = models.BooleanField(verbose_name=u'является публичной', default=False)
	
	objects = models.Manager()	
	publics = PublicManager()
	
	def get_title(self): return self.title
	def get_text(self): return self.text
	
	def __unicode__(self):
		return self.get_title()
		
	@models.permalink
	def get_absolute_url(self):
		return ('category_item_url', (), {'id':self.id})
		
	def save(self, *args, **kwargs):
		if self.parent:
			if self.parent.is_active == False:
				self.is_active = False
			if self.parent.is_public == False:
				self.is_public = False
				
		if self.is_active == False:
			self.get_descendants().update(is_active = False)
		if self.is_public == False:
			self.get_descendants().update(is_public = False)
		super(CategoryArticle, self).save(*args, **kwargs)
		
	class Meta: 
		verbose_name = u"категория"
		verbose_name_plural = u"категории статей"

class ArticleItem(MetaModel, ActiveSortModel, DateCreateModel, TextAnnouncementModelReq):
	def make_upload_path(instance, filename):
		return make_file_path(filename, u'upload/article/')
	
	category = models.ForeignKey(CategoryArticle, verbose_name=u'категория', related_name='products_category')
	title = models.CharField(max_length=100, verbose_name=u'заголовок')
	image = SorlImageField(max_length=500, upload_to=make_upload_path, verbose_name=u'изображение', help_text=u'рекомендованный размер изображения - 140px*140px')
	
	is_public = models.BooleanField(verbose_name=u'является публичной', default=False)
	
	objects = models.Manager()	
	publics = PublicManager()
	
	def get_title(self): return self.title
	def get_image(self): return self.image
	
	def __unicode__(self):
		return self.get_title()
		
	@models.permalink
	def get_absolute_url(self):
		return ('article_item_url', (), {'id':self.id})
		
	def small_image(self):
		if self.image:
			f = get_thumbnail(self.image, '100', crop='center', quality=99, format='PNG')
			html = '<a href="%s"><img src="%s" title="%s" /></a>'
			return html % (self.image.url, f.url, self.title)
		else: return u"Нет изображения"

	small_image.short_description = u"Изображение"
	small_image.allow_tags = True
		
	class Meta: 
		verbose_name = u"статья"
		verbose_name_plural = u"статьи"
		ordering = ['sort', 'created', 'id']
		
################################################################################################################
################################################################################################################