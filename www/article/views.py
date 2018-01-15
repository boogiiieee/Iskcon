# -*- coding: utf-8 -*-

from django.http import Http404
from django.views.generic import list_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.contrib.sitemaps import Sitemap

from django.conf import settings
from article.models import CategoryArticle, ArticleItem

##########################################################################
##########################################################################

#Для карты сайта
class ArticleSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.5
	
	def items(self):
		return ArticleItem.publics.all()
		
	def location(self, obj):
		return obj.get_absolute_url()
		
##########################################################################
##########################################################################


def all(request, id = None):
	try: page = int(request.GET.get('page', 1))
	except ValueError: page = 1
	cat_menu = None	
	
	if request.user.is_authenticated():
		cat_menu = CategoryArticle.activs.all()
		if id:
			try: id = int(id)
			except TypeError: raise Http404()
			
			try:
				obj = CategoryArticle.activs.get(id=id)
				objs = ArticleItem.activs.filter(category = obj)
			except:
				raise Http404()
		else:
			obj = None
			objs = ArticleItem.activs.filter(category__in = cat_menu)
	else:
		cat_menu = CategoryArticle.publics.all()
		if id:
			try: id = int(id)
			except TypeError: raise Http404()
			
			try:
				obj = CategoryArticle.publics.get(id=id)
				objs = ArticleItem.publics.filter(category = obj)
			except:
				raise Http404()
		else:
			obj = None
			objs = ArticleItem.publics.filter(category__in = cat_menu)

	
	return list_detail.object_list(
		request,
		queryset = objs,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'article/all.html',
		template_object_name = 'article',
		extra_context = {
			'cat': obj,
			'category_menu': cat_menu,
			'active':3,
		},
	)
	
##########################################################################
##########################################################################
	
def article_item(request, id):
	try:
		id = int(id)
	except TypeError:
		raise Http404()
	
	cat_menu = None
	
	if request.user.is_authenticated():	
		objs = ArticleItem.activs.all()
		cat_menu = CategoryArticle.activs.all()
	else: 
		objs = ArticleItem.publics.all()
		cat_menu = CategoryArticle.publics.all()
	
	try: item = objs.get(id = id)
	except: raise Http404()
	
	return render_to_response('article/item.html', {'active':3, 'item':item, 'category_menu': cat_menu}, RequestContext(request))
	
##########################################################################
##########################################################################