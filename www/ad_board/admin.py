# -*- coding: utf-8 -*-

from django.contrib import admin

from ad_board.models import CategoryAdBoard, AdBoardItem

################################################################################################################
################################################################################################################

class CategoryAdBoardAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_active', 'is_public', 'sort')
	search_fields = ('title',)
	list_filter = ('is_active', 'is_public' )
	list_editable = ('is_active', 'is_public', 'sort')
	
	fieldsets = (
		(None, {'fields': ('title', 'text', 'is_active', 'sort')},),
		(u'Мета-теги', {'classes': ('collapse',), 'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
	)
admin.site.register(CategoryAdBoard, CategoryAdBoardAdmin)

################################################################################################################
################################################################################################################

class AdBoardItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'category', 'cost', 'is_active', 'is_public', 'sort')
	search_fields = ('title',)
	list_filter = ('is_active', 'is_public', 'user', 'category')
	list_editable = ('is_active', 'is_public', 'sort')
	
admin.site.register(AdBoardItem, AdBoardItemAdmin)