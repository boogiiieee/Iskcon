# -*- coding: utf-8 -*-

from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from configuration.models import ConfigModel
from configuration.forms import ConfigForm

##########################################################################
##########################################################################

class ConfigModelAdmin(AdminImageMixin, admin.ModelAdmin):
	form = ConfigForm
	fieldsets = (
		(None, {'fields': ('site_name', 'image', 'is_active',)}),
		(u'Рассылка e-mail', {'fields': ('email_sign',)}),
		(None, {'fields': ('clear_cache_link',)}),
	)
	readonly_fields = ('clear_cache_link',)
	
	def clear_cache_link(self, obj):
		return u'<a href="/cache/clear_cache/">очистить</a>'
	clear_cache_link.short_description = u'Очистить кэш'
	clear_cache_link.allow_tags = True
	
	def has_add_permission(self, *args, **kwargs):
		return False
		
	def has_delete_permission(self, *args, **kwargs):
		return False
	
admin.site.register(ConfigModel, ConfigModelAdmin)

##########################################################################
##########################################################################