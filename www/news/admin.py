# -*- coding: utf-8 -*-

from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from news.models import NewsArticle

##########################################################################
##########################################################################

class NewsArticleAdmin(AdminImageMixin, admin.ModelAdmin):
	list_display = ('title', 'created', 'modified', 'is_active', 'is_public', 'sort', 'id')
	list_filter = ('is_active', 'created', 'is_public', 'is_active',)
	search_fields = ('title', )
	list_editable = ('is_active', 'is_public', 'sort')
	fieldsets = (
		(None, {'fields': ('title', 'image', 'announcement', 'text', 'is_active', 'is_public', 'sort')},),
		(u'Мета-теги', {'classes': ('collapse',), 'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
	)
	
admin.site.register(NewsArticle, NewsArticleAdmin)

##########################################################################
##########################################################################