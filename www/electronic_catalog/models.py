# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField as SorlImageField
from redactor.fields import RedactorField
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

from engine.models import make_file_path, MetaModel, ActiveSortModel, DateCreateModel

################################################################################################################
################################################################################################################

class PublicManager(models.Manager): 
	def get_query_set(self): 
		return super(PublicManager, self).get_query_set().filter(is_active=True, is_public = True)

class CategoryElectronicCatalog(MPTTModel, MetaModel, ActiveSortModel):
	parent = TreeForeignKey('self', verbose_name=u"родительская категория", blank=True, null=True, related_name='children_category_e_c')
	title = models.CharField(max_length=500, verbose_name=u'заголовок')
	text = RedactorField(max_length=1000, verbose_name=u"описание")
	
	is_public = models.BooleanField(verbose_name=u'является публичной', default=False)
	
	objects = models.Manager()	
	publics = PublicManager()
	
	def get_active_children(self):
		return self.get_children().filter(is_active=True,)
		
	def get_public_children(self):
		return self.get_children().filter(is_active=True, is_public = True)
		
	def get_title(self): return self.title
	def get_text(self): return self.text
	
	def __unicode__(self):
		return self.get_title()
		
	@models.permalink
	def get_absolute_url(self):
		return ('category_electronic_catalog_url', (), {'id':self.id})
		
	@models.permalink
	def get_order_url(self):
		return ('category_electronic_order_url', (), {'id':self.id})
		
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
		super(CategoryElectronicCatalog, self).save(*args, **kwargs)
		
	class Meta: 
		verbose_name = u"категория электронного каталога"
		verbose_name_plural = u"категории электронного каталога"


class ElectronicCatalogItem(MetaModel, ActiveSortModel, DateCreateModel):
	def make_upload_path(instance, filename):
		return u'upload/electronic_catalog/%s' % filename.lower()
		
	category = models.ForeignKey(CategoryElectronicCatalog, verbose_name=u'категория', related_name='сategory_rel_e_c')	
	
	is_public = models.BooleanField(verbose_name=u'публичное', default=False, help_text=u'Объявление будет доступно и для незарегистрированных пользователей.')
	
	objects = models.Manager()	
	publics = PublicManager()
	
	title = models.CharField(max_length=500, verbose_name=u'заголовок')
	announcement = models.TextField(max_length=10000, verbose_name=u"краткое описание")
	text = RedactorField(max_length=10000, verbose_name=u"полное описание")
	image = SorlImageField(max_length=500, upload_to=make_upload_path, verbose_name=u'изображение')
	cost = models.IntegerField(verbose_name='цена', default=0)
	
	def __unicode__(self):
		return u'%s' % self.title
		
	def get_title(self): return self.title
	def get_announcement(self): return self.announcement
	def get_text(self): return self.text
	def get_image(self): return self.image
	def get_cost(self): return self.cost
	def get_type_cost(self): return u'руб.'
	
	def get_all_cost(self):
		if self.get_cost():
			return u'%s %s' % (self.get_cost(), self.get_type_cost())
		else: return u'не указано'
	
	@models.permalink
	def get_absolute_url(self):
		return ('electronic_catalog_item_url', (), {'id':self.id})
		
	@models.permalink
	def get_order_url(self):
		return ('electronic_catalog_order_url', (), {'id':self.id})
		
	@models.permalink
	def get_profile_electronic_catalog_url(self):
		return ('profile_electronic_catalog_url', (), {})
		
	class Meta: 
		verbose_name = u'объявление электронного каталога'
		verbose_name_plural = u'объявления электронного каталога'
		ordering = ['sort', '-created', '-modified', '-id']
		
################################################################################################################
################################################################################################################