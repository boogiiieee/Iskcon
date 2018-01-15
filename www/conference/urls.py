# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('conference.views',
    url(r'^$', 'index', name='conference_index'),
    url(r'^group/user_list/$', 'group_user_list', name='conference_group_user_list'),
    
    url(r'^group/(?P<group_id>[0-9]+)/$', 'group', name='conference_group'),
    url(r'^group/(?P<group_id>[0-9]+)/subscribe/$', 'group_subscribe', name='conference_group_subscribe'),
    url(r'^group/(?P<group_id>[0-9]+)/(?P<user_id>[0-9]+)/subscribe/admin/$', 'group_subscribe_admin', name='conference_group_subscribe_admin'),
    url(r'^group/(?P<group_id>[0-9]+)/(?P<user_id>[0-9]+)/subscribe/admin/cancel/$', 'group_subscribe_admin_cancel', name='conference_group_subscribe_admin_cancel'),
    url(r'^group/(?P<group_id>[0-9]+)/subscribe/del/$', 'group_subscribe_del', name='conference_group_subscribe_del'),
    url(r'^group/(?P<group_id>[0-9]+)/(?P<user_id>[0-9]+)/subscribe/admin/del/$', 'group_subscribe_admin_del', name='conference_group_subscribe_admin_del'),
    url(r'^group/(?P<group_id>[0-9]+)/subscribe/frozen/$', 'group_subscribe_frozen', name='conference_group_subscribe_frozen'),
    url(r'^group/(?P<group_id>[0-9]+)/subscribe/frozen/del/$', 'group_subscribe_frozen_del', name='conference_group_subscribe_frozen_del'),
    
    url(r'^group/(?P<group_id>[0-9]+)/(?P<user_id>[0-9]+)/ban/$', 'ban', name='conference_ban'),
    url(r'^group/(?P<group_id>[0-9]+)/(?P<user_id>[0-9]+)/ban/del/$', 'ban_del', name='conference_ban_del'),
    
    url(r'^request/$', 'admin_contact', name='conference_admin_contact'),
    url(r'^request/(?P<req_id>[0-9]+)/del/$', 'admin_contact_del', name='conference_admin_contact_del'),
    url(r'^request/lider/$', 'admin_contact', name='conference_lider_contact'),
    
    url(r'^moderate/(?P<msg_id>[0-9]+)/ok/$', 'admin_moderate_ok', name='conference_admin_moderate_ok'),
    url(r'^moderate/(?P<msg_id>[0-9]+)/del/$', 'admin_moderate_del', name='conference_admin_moderate_del'),
    
    url(r'^create_email/$', 'create_email', name='conference_create_email'),
)