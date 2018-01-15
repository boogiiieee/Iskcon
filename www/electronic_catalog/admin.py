# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms

from mptt.admin import MPTTModelAdmin, MPTTChangeList
from mptt.forms import TreeNodeChoiceField

from electronic_catalog.models import CategoryElectronicCatalog, ElectronicCatalogItem

from engine.admin import MPTTAdminSaveFilter, ModelAdminSaveFilter
################################################################################################################
################################################################################################################

class CategoryElectronicCatalogAdmin(MPTTAdminSaveFilter):
	list_display = ('title', 'parent', 'is_active', 'is_public', 'sort')
	search_fields = ('title',)
	list_filter = ('is_active', 'parent', 'is_public' )
	list_editable = ('is_active', 'is_public', 'sort')
	
	fieldsets = (
		(None, {'fields': ('parent', 'title', 'text', 'is_active', 'sort')},),
		(u'Мета-теги', {'classes': ('collapse',), 'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
	)
admin.site.register(CategoryElectronicCatalog, CategoryElectronicCatalogAdmin)

################################################################################################################
################################################################################################################
class ElectronicCatalogItemAdminForm(forms.ModelForm):
	category = TreeNodeChoiceField(queryset=CategoryElectronicCatalog.tree.all(), label=u'Категория')
	class Meta:
		model = ElectronicCatalogItem
		
class ElectronicCatalogItemAdmin(admin.ModelAdmin):
	form = ElectronicCatalogItemAdminForm
	list_display = ('title', 'category', 'cost', 'is_active', 'is_public', 'sort')
	search_fields = ('title',)
	list_filter = ('is_active', 'is_public', 'category')
	list_editable = ('is_active', 'is_public', 'sort')
	
	fieldsets = (
		(None, {'fields': ('category', 'title', 'cost', 'image', 'announcement', 'text', 'is_active', 'is_public', 'sort')},),
		(u'Мета-теги', {'classes': ('collapse',), 'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
	)
	
admin.site.register(ElectronicCatalogItem, ElectronicCatalogItemAdmin)