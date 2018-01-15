# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from django.contrib.auth import views as auth_views
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from django.contrib.sitemaps import FlatPageSitemap
from news.views import NewsSitemap
from article.views import ArticleSitemap
from media_content.views import FotoItemSitemap, VideoItemSitemap, AudioItemSitemap
from electronic_catalog.views import ElectronicCatalogItemSitemap

sitemaps = {
    'flatpages': FlatPageSitemap,
    'foto': FotoItemSitemap,
    'video': VideoItemSitemap,
    'audio': AudioItemSitemap,
    'article': ArticleSitemap,
    'news': NewsSitemap,
    'electronic_catalog':ElectronicCatalogItemSitemap,
}

urlpatterns = patterns('',
    url(r'^', include('iskcon.urls')),
    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'registration/password_reset_form1.html', 'email_template_name':'registration/password_reset_email1.html'} ),
    url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name':'registration/password_reset_done1.html',} ),
    url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name':'registration/password_reset_confirm1.html',} ),
    url(r'^accounts/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name':'registration/password_reset_complete1.html',} ),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='auth_logout'),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/', include('registration.urls')),
    
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^', include('private_media.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    
    url(r'^redactor/', include('redactor.urls')),
    url(r'^captcha/', include('captcha.urls')),
    
    url(r'^news/', include('news.urls')),
    url(r'^article/', include('article.urls')),
    url(r'^ad_board/', include('ad_board.urls')),
    url(r'^electronic_catalog/', include('electronic_catalog.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    
    url(r'^', include('media_content.urls')),
    url(r'^forum/', include('forum.urls')),
    #url(r'^', include('multicasting.urls')),
    url(r'^conference/', include('conference.urls')),

    url(r'^cache/', include('clear_cache.urls')),

)
urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', 'django.views.static.serve', {'path':"/robots.txt", 'document_root':settings.MEDIA_ROOT, 'show_indexes': False}),
)
