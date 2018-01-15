# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms

from embed_video.admin import AdminVideoMixin
from mptt.admin import MPTTModelAdmin, MPTTChangeList
from mptt.forms import TreeNodeChoiceField

from media_content.models import CategoryMedia, CategoryFoto, FotoItem, \
    CategoryVideo, VideoItem, CategoryAudio, AudioItem

from engine.admin import MPTTAdminSaveFilter, ModelAdminSaveFilter
from sorl.thumbnail.admin import AdminImageMixin

##########################################################################
##########################################################################

class CategoryMediaAdmin(MPTTAdminSaveFilter):
    list_display = ('title', 'parent', 'is_active', 'is_public', 'sort')
    list_filter = ('is_active', 'parent')
    search_fields = ('title',)
    list_editable = ('is_active', 'is_public', 'sort')
    fieldsets = (
        (None, {'fields': ('parent', 'title', 'text', 'is_active', 'is_public', 'sort')},),
        (u'Мета-теги', {'classes': ('collapse',), 'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
    )

class MediaItemAdmin(AdminImageMixin, ModelAdminSaveFilter,):
    list_display = ('title', 'category', 'is_active', 'is_public', 'sort')
    list_filter = ('is_active', 'category')
    search_fields = ('title',)
    list_editable = ('is_active', 'is_public', 'sort')
    fieldsets = (
        (None, {'fields': ('category', 'title', 'file', 'text', 'is_active', 'is_public', 'sort')},),
        (u'Мета-теги', {'classes': ('collapse',), 'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
    )

class FotoItemAdminForm(forms.ModelForm):
    category = TreeNodeChoiceField(queryset=CategoryFoto.tree.all(), label=u'Категория')
    class Meta:
        model = FotoItem

class FotoItemAdmin(MediaItemAdmin,):
    form = FotoItemAdminForm


class VideoItemAdminForm(forms.ModelForm):
    category = TreeNodeChoiceField(queryset=CategoryVideo.tree.all(), label=u'Категория')

    class Meta:
        model = VideoItem


class VideoItemAdmin(AdminVideoMixin, MediaItemAdmin,):
    form = VideoItemAdminForm

    fieldsets = (
        (None, {
            'fields':
                ('category', 'title', 'text', 'is_active', 'is_public', 'sort')
        },),
        (u'Параметры для видео.', {
            'fields': ('file', ('rtmp_file', 'rtmp'), 'video_url', 'iframe', 'video_mms',),
            'description': u'Необходимо указать только <b>один</b> из предлагаемых параметров '
                           u'(<b>кроме параметров видео-потока</b>).<br><br>'
                           u'Если заполнено несколько параметров, то будет использован <b>первый</b> в списке.<br><br>',
        }),
        (u'Мета-теги', {
            'classes':
                ('collapse',), 'fields': ('meta_title', 'meta_description',
                                          'meta_keywords')
        }),
    )


class AudioItemAdminForm(forms.ModelForm):
    category = TreeNodeChoiceField(queryset=CategoryAudio.tree.all(), label=u'Категория')

    class Meta:
        model = AudioItem


class AudioItemAdmin(MediaItemAdmin,):
    form = AudioItemAdminForm

    fieldsets = (
        (None, {
            'fields':
                ('category', 'title', 'is_active', 'is_public', 'sort')
        },),
        (u'Параметры для аудио.', {
            'fields': ('file', 'stream', 'audio_mms',),
            'description': u'Необходимо указать только <b>один</b> из предлагаемых параметров.<br><br>'
                           u'Если заполнено несколько параметров, то будет использован <b>первый</b> в списке.<br><br>',
        }),
        (u'Мета-теги', {
            'classes':
                ('collapse',), 'fields': ('meta_title', 'meta_description',
                                          'meta_keywords')
        }),
    )

admin.site.register(CategoryFoto, CategoryMediaAdmin)
admin.site.register(CategoryVideo, CategoryMediaAdmin)
admin.site.register(CategoryAudio, CategoryMediaAdmin)
admin.site.register(FotoItem, FotoItemAdmin)
admin.site.register(VideoItem, VideoItemAdmin)
admin.site.register(AudioItem, AudioItemAdmin)


##########################################################################
##########################################################################