# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('multicasting.views',
	url(r'^accounts/profile/inbox/$', 'inbox', name='multicasting_url'),
	url(r'^accounts/profile/inbox/(?P<id>[0-9]+)/$', 'inbox_item', name='inbox_item_multicasting_url'),
	url(r'^accounts/profile/inbox/(?P<id>[0-9]+)/delete/$', 'inbox_item_delete', name='inbox_delete_multicasting_url'),
	url(r'^accounts/profile/outbox/$', 'outbox', name='multicasting_outbox_url'),
	
	url(r'^accounts/profile/outbox/(?P<id>[0-9]+)/$', 'outbox_item', name='outbox_item_multicasting_url'),
	url(r'^accounts/profile/outbox/(?P<id>[0-9]+)/delete/$', 'outbox_item_delete', name='outbox_delete_multicasting_url'),
	
	url(r'^accounts/profile/perm/$', 'perm', name='multicasting_perm_url'),
	url(r'^accounts/profile/perm_no_send/(?P<id>[0-9]+)/$', 'perm_no_send', name='multicasting_perm_no_send_url'),
	url(r'^accounts/profile/perm_yes_send/(?P<id>[0-9]+)/$', 'perm_yes_send', name='multicasting_perm_yes_send_url'),
	
	url(r'^accounts/profile/sms/add/$', 'add', name='add_multicasting_sms_url'),
)
