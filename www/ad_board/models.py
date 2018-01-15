# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField as SorlImageField
from redactor.fields import RedactorField

from engine.models import make_file_path, MetaModel, ActiveSortModel, DateCreateModel

################################################################################################################
################################################################################################################

class PublicManager(models.Manager): 
	def get_query_set(self): 
		return super(PublicManager, self).get_query_set().filter(is_active=True, is_public = True)

class CategoryAdBoard(MetaModel, ActiveSortModel):
	title = models.CharField(max_length=500, verbose_name=u'заголовок')
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
		return ('category_ad_board_url', (), {'id':self.id})
		
	@models.permalink
	def get_add_ad_url(self):
		return ('add_ad_board_url', (), {'id':self.id})
		
	class Meta: 
		verbose_name = u"категория объявлений"
		verbose_name_plural = u"категории объявлений"


class AdBoardItem(ActiveSortModel, DateCreateModel):
	def make_upload_path(instance, filename):
		if instance.user: return u'upload/%d/ad_board/%s' % (instance.user.id, filename.lower())
		else: return u'upload/ad_board/%s' % filename.lower()
		
	user = models.ForeignKey(User, verbose_name=u'пользователь', related_name='user_rel')
	category = models.ForeignKey(CategoryAdBoard, verbose_name=u'категория', related_name='сategory_rel')	
	
	is_public = models.BooleanField(verbose_name=u'публичное объявление', default=False, help_text=u'Объявление будет доступно и для незарегистрированных пользователей')
	
	objects = models.Manager()	
	publics = PublicManager()
	
	title = models.CharField(max_length=500, verbose_name=u'заголовок')
	text = RedactorField(max_length=10000, verbose_name=u"полное описание")
	image = SorlImageField(max_length=500, upload_to=make_upload_path, verbose_name=u'изображение')
	cost = models.IntegerField(verbose_name='цена', default=0)
	
	def __unicode__(self):
		return u'%s - %s' % (self.user, self.title)
		
	def get_title(self): return self.title
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
		return ('ad_board_item_url', (), {'id':self.id})
		
	@models.permalink
	def get_profile_ad_url(self):
		return ('profile_ad_url', (), {})
		
	@models.permalink
	def get_edit_url(self):
		return ('ad_edit_item_url', (), {'id':self.id})
		
	@models.permalink
	def get_delete_url(self):
		return ('ad_delete_item_url', (), {'id':self.id})
		
	class Meta: 
		verbose_name = u'объявление'
		verbose_name_plural = u'объявления'
		ordering = ['sort', '-created', '-modified', '-id']
		
################################################################################################################
################################################################################################################