# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('ad_board.views',
	url(r'^$', 'full', name='ad_board_url'),
	url(r'^category/(?P<id>[0-9]+)/$', 'category', name='category_ad_board_url'),
	url(r'^(?P<id>[0-9]+)/$', 'item', name='ad_board_item_url'),
	
	url(r'^category/(?P<id>[0-9]+)/add/$', 'add', name='add_ad_board_url'),
)
