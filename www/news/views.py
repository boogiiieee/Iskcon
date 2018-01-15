# -*- coding: utf-8 -*-

from django.http import Http404
from django.views.generic import list_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps import Sitemap

from news.conf import settings as conf
from news.models import NewsArticle

##########################################################################
##########################################################################

#Для карты сайта
class NewsSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.5
	
	def items(self):
		return NewsArticle.publics.all()
		
	def location(self, obj):
		return obj.get_absolute_url()
		
##########################################################################
##########################################################################

def all(request):
	try: page = int(request.GET.get('page', 1))
	except ValueError: page = 1
	
	if request.user.is_authenticated():	objs = NewsArticle.activs.all()
	else: objs = NewsArticle.publics.all()

	return list_detail.object_list(
		request,
		queryset = objs,
		paginate_by = conf.PAGINATE_BY,
		page = page,
		template_name = 'news/news.html',
		template_object_name = 'news',
		extra_context = {
			'active':2,
		},
	)
	
##########################################################################
##########################################################################

def full(request, id):
	try:
		id = int(id)
	except TypeError:
		raise Http404()
		
	if request.user.is_authenticated():	objs = NewsArticle.activs.all()
	else: objs = NewsArticle.publics.all()
	
	try: item = objs.get(id = id)
	except: raise Http404()
		
	return render_to_response('news/item.html', {'active':2, 'item':item}, RequestContext(request))

	
##########################################################################
##########################################################################