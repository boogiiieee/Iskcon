# -*- coding: utf-8 -*-

from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from django.conf import settings
from django.contrib.sitemaps import Sitemap

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from electronic_catalog.models import CategoryElectronicCatalog, ElectronicCatalogItem
from electronic_catalog.forms import AddElectronicCatalogForm

##########################################################################
##########################################################################

#Для карты сайта
class ElectronicCatalogItemSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.5
	
	def items(self):
		return ElectronicCatalogItem.publics.all()
		
	def location(self, obj):
		return obj.get_absolute_url()
		
################################################################################################################
################################################################################################################


def full(request):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	if request.user.is_authenticated():
		cat_menu = CategoryElectronicCatalog.activs.all()
		objs = ElectronicCatalogItem.activs.filter(category__in = cat_menu)
	else:
		cat_menu = CategoryElectronicCatalog.publics.all()
		objs = ElectronicCatalogItem.publics.filter(category__in = cat_menu)
	
	return object_list(request,
		queryset = objs,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'electronic_catalog/full.html',
		template_object_name = 'items',
		extra_context = {
			'active':11,
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
		try: cat = CategoryElectronicCatalog.activs.get(id=id)
		except:	raise Http404()
		objs = ElectronicCatalogItem.activs.filter(category__in = [cat,]+list(cat.get_active_children()))
	else:
		try: cat = CategoryElectronicCatalog.publics.get(id=id)
		except:	raise Http404()
		objs = ElectronicCatalogItem.publics.filter(category__in = [cat,]+list(cat.get_public_children()))
	
	return object_list(request,
		queryset = objs,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'electronic_catalog/category.html',
		template_object_name = 'items',
		extra_context = {
			'active':11,
			'cat': cat,
		},
	)

@render_to('electronic_catalog/item.html')
def item(request, id):
	if request.user.is_authenticated():
		try: item = ElectronicCatalogItem.activs.get(id=id)
		except:	raise Http404()
	else:
		try: item = ElectronicCatalogItem.publics.get(id=id)
		except:	raise Http404()
		
	return {
		'item': item,
		'active':11,
	}
