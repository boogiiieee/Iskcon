# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode, iri_to_uri
from django.contrib.admin.filters import RelatedFieldListFilter
from django.contrib.admin.util import get_model_from_relation
from django.utils.http import urlencode, urlquote

from django.core.cache import cache 
from django.conf import settings
################################################################################################################
################################################################################################################

#Сортировка пользовательского фильтра по названию
class SortTitleFilterSpec(RelatedFieldListFilter):
	def __init__(self, f, request, params, model, model_admin, field_path=None):
		super(SortTitleFilterSpec, self).__init__(f, request, params, model, model_admin, field_path=field_path)
		self.lookup_choices = sorted(f.get_choices(include_blank=False),key=lambda x: x[1])
		
################################################################################################################
################################################################################################################

#Фильтр для вывода дерева mptt
class MpttParentFieldFilterSpec(RelatedFieldListFilter):
	mptt_parent_field_filter = True
	
	def __init__(self, f, request, params, model, model_admin, field_path=None):
		super(MpttParentFieldFilterSpec, self).__init__(f, request, params, model, model_admin, field_path=field_path)
		
		from shop.models import Category
		queryset = Category.objects.all()
		self.lookup_choices = [(x._get_pk_val(), x) for x in queryset]
		
		other_model = get_model_from_relation(f)
		if isinstance(f, (models.ManyToManyField, models.related.RelatedObject)): self.lookup_title = other_model._meta.verbose_name
		else: self.lookup_title = f.verbose_name
		rel_name = other_model._meta.pk.name
		self.lookup_kwarg = '%s__%s__in' % (self.field_path, rel_name)
		
		self.lookup_val = request.GET.get(self.lookup_kwarg, None)
		self.lookup_val_isnull = request.GET.get(self.lookup_kwarg_isnull, None)
		
	def choices(self, cl):
		from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
		
		yield {
			'selected': self.lookup_val is None and not self.lookup_val_isnull,
			'query_string': cl.get_query_string(
				{},
				[self.lookup_kwarg, self.lookup_kwarg_isnull]
			),
			'display': _('All')
		}
		try: s = self.lookup_val.split(',')[0]
		except: s = None

		name = u'%s' % self.field_path
		cache_name = u'mptt_filter_%s%s' % (s, name)
		cache_time = settings.CACHE_TIME
		cache_html = cache.get(cache_name)
		if cache_html:
			yield cache_html
		else:
			deph, tmp, html = 0, -1, u''
			for pk_val, val in self.lookup_choices:
				deph = val.get_parents().count()
				
				hide = u' style="display:none"' if deph else u''
				selected = u' class="selected"' if s == smart_unicode(pk_val) else u''
				icon = u'<a class="mptt_link" href="#">&#9658;</a>' if val.get_children().count() else u''

				pk_vals = '%d' % pk_val
				post_pk_vals = ','.join([u'%d'%i.pk for i in val.get_all_subcategory()])
				if post_pk_vals: pk_vals = pk_vals + ',' + post_pk_vals

				query_string = cl.get_query_string({self.lookup_kwarg: pk_vals}, [self.lookup_kwarg_isnull])
				link = u'%s=%s;' %(self.lookup_kwarg, urlquote(pk_vals))
				a = u'<a class="link" href="%s">%s</a>' % (link, val.title)
				
				if deph > tmp: html += u'<ul%s><li%s>%s%s' % (hide, selected, icon, a)
				elif deph == tmp: html += u'</li><li%s>%s%s' % (selected, icon, a)
				elif deph < tmp:
					for i in range(tmp-deph): html += u'</li></ul>'
					html += u'</li><li%s>%s%s' % (selected, icon, a)
					
				tmp = deph
			for i in range(deph+1): html += u'</li></ul>'
			
			cache.set(cache_name, html, cache_time)
			yield html
			
		if isinstance(self.field, models.related.RelatedObject) and self.field.field.null or hasattr(self.field, 'rel') and self.field.null:
			yield {
				'selected': bool(self.lookup_val_isnull),
				'query_string': cl.get_query_string(
					{self.lookup_kwarg_isnull: 'True'},
					[self.lookup_kwarg]),
				'display': EMPTY_CHANGELIST_VALUE
			}

################################################################################################################
################################################################################################################
