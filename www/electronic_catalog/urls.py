# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('electronic_catalog.views',
	url(r'^$', 'full', name='electronic_catalog_url'),
	url(r'^category/(?P<id>[0-9]+)/$', 'category', name='category_electronic_catalog_url'),
	url(r'^(?P<id>[0-9]+)/$', 'item', name='electronic_catalog_item_url'),
)
