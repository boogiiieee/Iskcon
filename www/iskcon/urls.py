# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

from iskcon.forms import MyRegistrationForm


urlpatterns = patterns('iskcon.views',
    url(r'^$', 'index', name='index'),
    url(r'^contacts/$', 'contacts', name='contacts'),
    url(r'^order/(?P<id>[0-9]+)/$', 'order',
        name='electronic_catalog_order_url'),
    
    url(r'^accounts/profile/$', 'profile_views', name='profile_url'),
    url(r'^accounts/e-mail/$', 'profile_email', name='profile_email'),
    url(r'^accounts/change-password/$', 'profile_change_password',
        name='profile_change_password_url'),
    
    url(r'^accounts/profile/ads/$', 'profile_ad', name='profile_ad_url'),
    url(r'^accounts/profile/ads/(?P<id>[0-9]+)/$', 'profile_ad_edit',
        name='ad_edit_item_url'),
    url(r'^accounts/profile/ads/(?P<id>[0-9]+)/delete/$', 'profile_ad_delete',
        name='ad_delete_item_url'),
    
    url(r'^accounts/profile/orders/$', 'profile_order',
        name='profile_order_url'),
    
    url(r'^accounts/profile/forum/thread/$', 'profile_thread',
        name='profile_thread_url'),
    url(r'^accounts/profile/forum/post/$', 'profile_post',
        name='profile_post_url'),
)

urlpatterns += patterns('',
    url(r'^accounts/register/$', 'registration.views.register',
        {'form_class':MyRegistrationForm}, name='registration_register'),
)
