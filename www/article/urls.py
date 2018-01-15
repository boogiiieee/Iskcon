from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('article.views',
	url(r'^$', 'all', name='article_url'),	
	url(r'^category/(?P<id>[0-9]{1,4})/$', 'all', name='category_item_url'),
	url(r'^(?P<id>[0-9]{1,4})/$', 'article_item', name='article_item_url'),
)