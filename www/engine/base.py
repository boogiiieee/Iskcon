# -*- coding: utf-8 -*-

from django.utils.html import mark_safe
from django.contrib.admin.util import lookup_needs_distinct, label_for_field
from django.db.models.related import RelatedObject
from django.db import models
import operator

SEARCH_VAR = 'q'

##########################################################################
##########################################################################

class TableModel():
	def __init__(self, qs, model, list_display=(), search_fields=()):
		self.qs = qs
		self.model = model
		self.opts = model._meta
		self.list_display = list_display
		self.search_fields = search_fields
		
	def header_list(self):
		u'''Возврвщает заголовки столбцов'''
		for i, field_name in enumerate(self.list_display):
			label = label_for_field(field_name, self.model)
			yield {'text': label}
				
	def row_list(self, item):
		u'''Возврвщает значения атрибутов строки'''
		for field_name in self.list_display:
			value = getattr(item, field_name, None)
			
			if type(value) is bool:
				value = u'<i class="icon-ok-sign" style="color:green"></i>' if value else u'<i class="icon-minus-sign" style="color:red"></i>'
				value = mark_safe(value)
				
			yield {'text': value}
			
	def get_queryset(self, request):
		u'''Модифицирует self.qs. Поиск.'''
		query = request.GET.get(SEARCH_VAR, '')
		qs = self.qs

		def construct_search(field_name):
			if field_name.startswith('^'):
				return "%s__istartswith" % field_name[1:]
			elif field_name.startswith('='):
				return "%s__iexact" % field_name[1:]
			elif field_name.startswith('@'):
				return "%s__search" % field_name[1:]
			else:
				return "%s__icontains" % field_name
		
		if self.search_fields and query:
			orm_lookups = [construct_search(str(search_field)) for search_field in self.search_fields]
			for bit in query.split():
				or_queries = [models.Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
				qs = qs.filter(reduce(operator.or_, or_queries))
				
			for search_spec in orm_lookups:
				if lookup_needs_distinct(self.opts, search_spec):
					qs = qs.distinct()
					break
				
		return qs
		
		
##########################################################################
##########################################################################