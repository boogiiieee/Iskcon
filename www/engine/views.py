# -*- coding: utf-8 -*-

from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.list_detail import object_list
from django.contrib import messages
from django.conf import settings

from annoying.utils import HttpResponseReload
from annoying.functions import get_object_or_None

from engine.base import TableModel

PAGINATE_BY = getattr(settings, 'ENGINE_PAGINATE_BY', 50)

##########################################################################
##########################################################################

#Список
def item_list(request, queryset, list_display, template_name, extra_context={}, search_fields=()):
	try: page = int(request.GET.get('page', 1))
	except ValueError: page = 1
	
	table = TableModel(
		qs = queryset,
		model = queryset.model,
		list_display = list_display,
		search_fields = search_fields,
	)
	
	c = {
		'table': table,
	}
	
	if extra_context:
		for key, value in extra_context.items():
			c[key] = value
	
	return object_list(request,
		queryset = table.get_queryset(request),
		paginate_by = PAGINATE_BY,
		page = page,
		template_name = template_name,
		template_object_name = 'item',
		extra_context = c,
	)
	
##########################################################################
##########################################################################

#Добавить
def item_add(request, Model, Form, template_name, extra_context={}, *args, **kwargs):
	obj = Model(*args, **kwargs)
	
	form = Form(request.POST or None, request.FILES or None, instance=obj)
	if form.is_valid():
		form.save()

		messages.add_message(request, messages.SUCCESS, u'Запись добавлена.')
		return HttpResponseRedirect(obj.get_absolute_url())
		
	c = RequestContext(request, {'form':form})
	
	if extra_context:
		for key, value in extra_context.items():
			c[key] = value

	t = loader.get_template(template_name)
	return HttpResponse(t.render(c))
	
##########################################################################
##########################################################################
	
#Изменить
def item_edit(request, obj, Form, template_name, Formset=None, extra_context={}, redirect_url=None):
	form = Form(request.POST or None, request.FILES or None, instance=obj)
	formset = None
	if not Formset is None:
		formset = Formset(request.POST or None, request.FILES or None, instance=obj)
		
	if form.is_valid():
		save = False
		
		if formset:
			if formset.is_valid():
				form.save()
				formset.save()
				save = True
		else:
			form.save()
			save = True
			
		if save:
			messages.add_message(request, messages.SUCCESS, u'Запись сохранена.')
			
			if redirect_url:
				return HttpResponseRedirect(redirect_url)
			else:
				return HttpResponseReload(request)
			
	c = RequestContext(request, {'obj':obj, 'form':form, 'formset':formset})
	
	if extra_context:
		for key, value in extra_context.items():
			c[key] = value

	t = loader.get_template(template_name)
	return HttpResponse(t.render(c))
	
##########################################################################
##########################################################################
	
#Удалить
def item_del(request, obj):
	url = obj.get_list_url()
	obj.delete()
	
	messages.add_message(request, messages.SUCCESS, 'Запись удалена.')
	return HttpResponseRedirect(url)
	
##########################################################################
##########################################################################
