# -*- coding: utf-8 -*-

from django.http import Http404
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.contrib.sitemaps import Sitemap

from django.conf import settings
from media_content.models import CategoryMedia, CategoryFoto, FotoItem, CategoryVideo, VideoItem, CategoryAudio, AudioItem
##########################################################################
##########################################################################

#Для карты сайта
class FotoItemSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return FotoItem.publics.all()

    def location(self, obj):
        return obj.get_absolute_url()

class VideoItemSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return VideoItem.publics.all()

    def location(self, obj):
        return obj.get_absolute_url()

class AudioItemSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return AudioItem.publics.all()

    def location(self, obj):
        return obj.get_absolute_url()

##########################################################################
##########################################################################

def all(request, model, cat_model, id = None, active=None):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    if request.user.is_authenticated():
        cat_menu = cat_model.activs.all()
        if id:
            try:
                id = int(id)
            except TypeError:
                raise Http404()
            try:
                obj = cat_model.activs.get(id=id)
            except:
                raise Http404()
            objs = model.activs.filter(category__in = [obj,]+list(obj.get_active_children()))
        else:
            obj = None
            objs = model.activs.all()[:10]
    else:
        cat_menu = cat_model.publics.all()
        if id:
            try:
                id = int(id)
            except TypeError:
                raise Http404()
            try:
                obj = cat_model.publics.get(id=id)
            except:
                raise Http404()
            objs = model.publics.filter(category__in = [obj,]+list(obj.get_public_children()))
        else:
            obj = None
            objs = model.publics.all()[:10]
    return list_detail.object_list(
        request,
        queryset = objs,
        paginate_by = settings.PAGINATE_BY,
        page = page,
        template_name = 'media_content/all.html',
        template_object_name = 'article',
        extra_context = {
            'cat': obj,
            'category_menu': cat_menu,
            'active':active,
        },
    )

##########################################################################
##########################################################################

@render_to('media_content/item.html')	
def item(request, id, model, cat_model, active=None):
    cat_menu = None

    if request.user.is_authenticated():
        objs = model.activs.all()
        cat_menu = cat_model.activs.all()
    else:
        objs = model.publics.all()
        cat_menu = cat_model.publics.all()

    try: item = objs.get(id = id)
    except: raise Http404()

    return {
        'item': item,
        'category_menu': cat_menu,
        'active':active,
    }

##########################################################################
##########################################################################