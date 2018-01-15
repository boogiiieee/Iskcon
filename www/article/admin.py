# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from sorl.thumbnail.admin import AdminImageMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.filters import FieldListFilter

from mptt.admin import MPTTModelAdmin, MPTTChangeList
from mptt.forms import TreeNodeChoiceField

from article.models import ArticleItem, CategoryArticle

from engine.admin import MPTTAdminSaveFilter, ModelAdminSaveFilter

#######################################################################################################################
#######################################################################################################################

#Категории
class CategoryArticleAdmin(MPTTAdminSaveFilter):
	list_display = ('title', 'parent', 'is_active', 'is_public', 'sort', 'id')
	search_fields = ('title',)
	list_filter = ('is_active', 'parent', 'is_active', 'is_public')
	list_editable = ('is_active', 'is_public', 'sort')
	
	fieldsets = (
		(None, {'fields': ('parent', 'title', 'text', 'is_active', 'sort')},),
		(u'Мета-теги', {'classes': ('collapse',), 'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
	)

admin.site.register(CategoryArticle, CategoryArticleAdmin)

#Статья
class ArticleItemAdminForm(forms.ModelForm):
	category = TreeNodeChoiceField(queryset=CategoryArticle.tree.all(), label=u'Категория')
	class Meta:
		model = ArticleItem
		
class ArticleItemAdmin(AdminImageMixin, ModelAdminSaveFilter,):
	form = ArticleItemAdminForm
	list_display = ('title', 'category', 'small_image', 'is_active', 'is_public', 'sort', 'id')
	search_fields = ('title',)
	list_filter = ('is_active', 'is_public', 'category')
	redonly_fields = ('small_image',)
	list_editable = ('is_active', 'is_public', 'sort')
	
	fieldsets = (
		(None, {'fields': ('category', 'title', 'image', 'announcement', 'text', 'is_active', 'is_public', 'sort')},),
		(u'Мета-теги', {'classes': ('collapse',), 'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
	)

admin.site.register(ArticleItem, ArticleItemAdmin)

#######################################################################################################################
#######################################################################################################################