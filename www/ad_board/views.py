# -*- coding: utf-8 -*-

from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from django.conf import settings

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from ad_board.models import CategoryAdBoard, AdBoardItem
from ad_board.forms import AddAdBoardForm

################################################################################################################
################################################################################################################


def full(request):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	if request.user.is_authenticated():
		cat_menu = CategoryAdBoard.activs.all()
		objs = AdBoardItem.activs.filter(category__in = cat_menu)
	else:
		cat_menu = CategoryAdBoard.publics.all()
		objs = AdBoardItem.publics.filter(category__in = cat_menu)
	
	return object_list(request,
		queryset = objs,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'ad_board/full.html',
		template_object_name = 'items',
		extra_context = {
			'active':10,
		},
	)
	
################################################################################################################
################################################################################################################


def category(request, id):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	try: id = int(id)
	except TypeError: raise Http404()
		
	if request.user.is_authenticated():
		try: cat = CategoryAdBoard.activs.get(id=id)
		except:	raise Http404()
		objs = AdBoardItem.activs.filter(category = cat)
	else:
		try: cat = CategoryAdBoard.publics.get(id=id)
		except:	raise Http404()
		objs = AdBoardItem.publics.filter(category = cat)
	
	return object_list(request,
		queryset = objs,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'ad_board/category.html',
		template_object_name = 'items',
		extra_context = {
			'active':10,
			'cat': cat,
		},
	)

@render_to('ad_board/item.html')
def item(request, id):
	if request.user.is_authenticated():
		try: item = AdBoardItem.activs.get(id=id)
		except:	raise Http404()
	else:
		try: item = AdBoardItem.publics.get(id=id)
		except:	raise Http404()
		
	return {
		'item': item,
		'active':10,
	}
	
@login_required
@render_to('ad_board/add.html')
def add(request, id):
	try:
		id = int(id)
	except TypeError:
		raise Http404()
		
	try:
		cat = CategoryAdBoard.activs.get(id=id)
	except:
		raise Http404()
		
	obj = AdBoardItem(user=request.user, category = cat)
	form = AddAdBoardForm(request.POST or None, request.FILES or None, instance=obj)
	if form.is_valid():
		form.save()
		messages.add_message(request, messages.SUCCESS, u'Объявление успешно добавлено.')
		return HttpResponseRedirect(u'%s' % cat.get_absolute_url())
	return {
		'form': form,
		'cat': cat,
		'active':10,
	}