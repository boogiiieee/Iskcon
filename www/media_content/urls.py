from django.conf.urls.defaults import *

from media_content.models import CategoryFoto, FotoItem, CategoryVideo, VideoItem, CategoryAudio, AudioItem

urlpatterns = patterns('media_content.views',
    url(r'^foto/$', 'all', {'model':FotoItem, 'cat_model':CategoryFoto, 'active':4}, name='foto_url'),
    url(r'^foto/category/(?P<id>[0-9]{1,4})/$', 'all', {'model':FotoItem, 'cat_model':CategoryFoto, 'active':4}, name='foto_category_url'),
    url(r'^foto/(?P<id>[0-9]{1,4})/$', 'item', {'model':FotoItem, 'cat_model':CategoryFoto, 'active':4}, name='foto_item_url'),

    url(r'^video/$', 'all', {'model':VideoItem, 'cat_model':CategoryVideo, 'active':5}, name='video_url'),
    url(r'^video/category/(?P<id>[0-9]{1,4})/$', 'all', {'model':VideoItem, 'cat_model':CategoryVideo, 'active':5}, name='video_category_url'),
    url(r'^video/(?P<id>[0-9]{1,4})/$', 'item', {'model':VideoItem, 'cat_model':CategoryVideo, 'active':5}, name='video_item_url'),

    url(r'^audio/$', 'all', {'model':AudioItem, 'cat_model':CategoryAudio, 'active':6}, name='audio_url'),
    url(r'^audio/category/(?P<id>[0-9]{1,4})/$', 'all', {'model':AudioItem, 'cat_model':CategoryAudio, 'active':6}, name='audio_category_url'),
    url(r'^audio/(?P<id>[0-9]{1,4})/$', 'item', {'model':AudioItem, 'cat_model':CategoryAudio, 'active':6}, name='audio_item_url'),
)