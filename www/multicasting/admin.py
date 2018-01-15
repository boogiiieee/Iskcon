# -*- coding: utf-8 -*-

from django.contrib import admin

from multicasting.models import MessagesMulticasting, GroupPermMulticasting, RecipientMulticasting

################################################################################################################
################################################################################################################

class GroupPermMulticastingAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_active', 'sort')
	search_fields = ('title',)
	list_filter = ('is_active',)
	filter_horizontal = ['user', 'leader']
	list_editable = ('is_active', 'sort')
	fieldsets = (
		(None, {'fields': ('title', 'user', 'leader', 'is_active', 'sort')},),
	)
admin.site.register(GroupPermMulticasting, GroupPermMulticastingAdmin)

################################################################################################################
################################################################################################################

# class AdBoardItemAdmin(admin.ModelAdmin):
	# list_display = ('title', 'user', 'category', 'cost', 'is_active', 'is_public', 'sort')
	# search_fields = ('title',)
	# list_filter = ('is_active', 'is_public', 'user', 'category')
	# list_editable = ('is_active', 'is_public', 'sort')
	
# admin.site.register(AdBoardItem, AdBoardItemAdmin)