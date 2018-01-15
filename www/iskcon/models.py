# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
import re, os
from pytils.translit import slugify

from threadmail import threading_send_mail

from engine.models import make_file_path, MetaModel, ActiveSortModel, DateCreateModel

from electronic_catalog.models import ElectronicCatalogItem

##################################################################################################	
##################################################################################################

#Анкета пользователя		
class UserProfile(models.Model):
	def make_upload_path(instance, filename):
		name, extension = os.path.splitext(filename)
		filename = u'%s%s' % (slugify(name), extension)
		return u'upload/user_profile/%d/%s' % (instance.user.id, filename.lower())
		
	user = models.OneToOneField(User, primary_key=True)
	file = models.FileField(upload_to=make_upload_path, verbose_name=u"фото", blank=True, null=True)
	phone = models.CharField(max_length=100, verbose_name=u'телефон', blank=True, null=True)
	#is_email = models.BooleanField(verbose_name=u'Получать уведомление на email о ЛС', default=True)
	#is_send_ls = models.BooleanField(verbose_name=u'Может отправлять ЛС', default=True)
	
	def get_user(self): return self.user
	def get_image(self): return self.file
	
	def __unicode__(self):
		return self.get_user().username
 
	class Meta: 
		verbose_name = u'карточка пользователя'
		verbose_name_plural = u'карточки пользователей'
		
def create_user_profile(sender, instance, created, **kwargs):   
	profile, created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)
	
##################################################################################################	
##################################################################################################

#Мои заказы

STATUS_ORDER = [
	(u'Принят', u'Принят'),
	(u'Готов', u'Готов и ожидает в офисе'),
	(u'Выдан', u'Выдан'),
]
class Order(ActiveSortModel, DateCreateModel):
	user = models.ForeignKey(User, verbose_name=u'пользователь', related_name='order_user_rel')
	product = models.ForeignKey(ElectronicCatalogItem, verbose_name=u"заказ", related_name='order_rel')
	status = models.CharField(max_length=10, verbose_name=u'статус', choices=STATUS_ORDER)
	cost = models.IntegerField(verbose_name='стоимость заказа', default=0)
	comment = models.TextField(max_length=10000, verbose_name=u'комментарий', blank=True, help_text=u'отображается только в административном интерфейсе')
	
	def __unicode__(self):
		return u'%s - %s' % (self.user, self.product.title)
		
	def get_title(self): return u'Заказ №%d - %s' % (self.id, self.product.get_title())
	
	@models.permalink
	def get_absolute_url(self):
		return ('order_item_url', (), {'id':self.id})
		
	@models.permalink
	def get_product_url(self):
		return ('electronic_catalog_item_url', (), {'id':self.product.id})
		
	def get_user_name(self):
		if self.user.get_full_name():
			return self.user.get_full_name()
		return self.user
		
	def get_user_email(self):
		return self.user.email
		
	def get_user_phone(self):
		return self.user.get_profile().phone
	
	def get_created_at(self):
		return self.created
		
	def get_cost(self):
		return self.cost
		
			
	def save(self, *args, **kwargs):
		if self.id:
			if Order.objects.get(id=self.id).status!=self.status:
				current_site = Site.objects.get_current()
				domain = current_site.domain
				if self.user.email:
					threading_send_mail('mail/order/change_status.html', u'Статус Вашего заказа на сайте %s был изменен' % domain, [self.user.email,], {'obj':self, 'domain':domain})
		super(Order, self).save(*args, **kwargs)

	class Meta: 
		verbose_name = u'заказ из электронного каталога'
		verbose_name_plural = u'заказы из электронного каталога'
		ordering = ['-status', 'sort', '-created', '-modified', '-id']
