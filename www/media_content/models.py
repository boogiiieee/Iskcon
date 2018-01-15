# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError

from embed_video.fields import EmbedVideoField
from sorl.thumbnail import ImageField as SorlImageField
from sorl.thumbnail.shortcuts import get_thumbnail, delete

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from redactor.fields import RedactorField	
from engine.models import make_file_path, MetaModel, ActiveSortModel, DateCreateModel, Article1Model

import re
import os


class PublicManager(models.Manager): 
    def get_query_set(self):
        return super(PublicManager, self).get_query_set().filter(is_active=True, is_public = True)

class CategoryMedia(MPTTModel, MetaModel, ActiveSortModel):
    parent = TreeForeignKey('self', verbose_name=u"родительская категория", blank=True, null=True, related_name='children_category')
    title = models.CharField(max_length=100, verbose_name=u'заголовок')
    text = RedactorField(max_length=1000, verbose_name=u"текст")

    is_public = models.BooleanField(verbose_name=u'является публичной', default=False)

    objects = models.Manager()
    publics = PublicManager()

    def get_title(self): return self.title
    def get_text(self): return self.text

    def get_active_children(self):
        return self.get_children().filter(is_active=True,)

    def get_public_children(self):
        return self.get_children().filter(is_active=True, is_public = True)

    def __unicode__(self):
        return self.get_title()

    def save(self, *args, **kwargs):
        if self.parent:
            if self.parent.is_active == False:
                self.is_active = False
            if self.parent.is_public == False:
                self.is_public = False

        if self.is_active == False:
            self.get_descendants().update(is_active = False)
        if self.is_public == False:
            self.get_descendants().update(is_public = False)
        super(CategoryMedia, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class CategoryFoto(CategoryMedia):
    def is_image(self): return True
    @models.permalink
    def get_absolute_url(self):
        return ('foto_category_url', (), {'id':self.id})

    class Meta:
        verbose_name = u"категория фото"
        verbose_name_plural = u"категории фото"

class FotoItem(Article1Model):
    def make_upload_path(instance, filename):
        return make_file_path(filename, u'upload/media-content/foto/')

    category = models.ForeignKey(CategoryFoto, verbose_name=u'категория', related_name='media_category')
    file = SorlImageField(max_length=500, upload_to=make_upload_path, verbose_name=u'изображение')

    is_public = models.BooleanField(verbose_name=u'является публичной', default=False)

    objects = models.Manager()
    publics = PublicManager()

    def get_image(self): return self.file
    
    def __unicode__(self):
        return self.get_title()

    @models.permalink
    def get_absolute_url(self):
        return ('foto_item_url', (), {'id':self.id})

    def clean(self):
        r = re.compile("^.*((\.jpg$)|(\.jpeg$)|(\.png$)|(\.bmp$)|(\.gif$))", re.IGNORECASE)
        if self.file:
            if not r.findall(os.path.split(self.file.url)[1]):
                raise ValidationError(u"Некорректный тип файла.")

    def small_image(self):
        if self.file:
            f = get_thumbnail(self.file, '100', crop='center', quality=99, format='PNG')
            html = '<a href="%s"><img src="%s" title="%s" /></a>'
            return html % (self.file.url, f.url, self.title)
        else: return u"Нет изображения"

    small_image.short_description = u"Изображение"
    small_image.allow_tags = True

    class Meta:
        verbose_name = u"фото"
        verbose_name_plural = u"фото"


class CategoryVideo(CategoryMedia):	
    def is_video(self):
        return True

    @models.permalink
    def get_absolute_url(self):
        return ('video_category_url', (), {'id':self.id})

    class Meta:
        verbose_name = u"категория видео"
        verbose_name_plural = u"категории видео"

class VideoItem(Article1Model):
    def make_upload_path(instance, filename):
        return make_file_path(filename, u'upload/media-content/video/')

    category = models.ForeignKey(CategoryVideo, verbose_name=u'категория',
                                 related_name='media_category')

    file = models.FileField(upload_to=make_upload_path, verbose_name=u'файл',
                            blank=True)
    video_url = EmbedVideoField(verbose_name=u'видео-ссылка', blank=True,
                                help_text=u'Ссылка, получаемая с YouTube или Vimeo.')
    rtmp_file = models.CharField(max_length=100, verbose_name=u'Файл видео-потока',
                                 blank=True,
                                 help_text=u'Файл вида: at16112014')
    rtmp = models.CharField(max_length=100, verbose_name=u'ссылка видео-потока',
                            blank=True,
                            help_text=u'Ссылка вида: rtmp://195.62.63.238/spb/')
    iframe = models.CharField(max_length=500, verbose_name=u'код IFrame',
                              blank=True)
    video_mms = models.CharField(max_length=100, blank=True,
                           verbose_name=u'ссылка для открытия во внешнем проигрывателе',
                           help_text=u'Ссылка вида: mms://195.62.63.238/tv_zolotoy_vek')

    is_public = models.BooleanField(verbose_name=u'является публичной', default=False)

    objects = models.Manager()
    publics = PublicManager()

    def get_file_url(self):
        if self.file:
            return self.file.url
        return False
        
    def __unicode__(self):
        return self.get_title()


    def get_params(self):
        if self.file or self.video_url or (self.rtmp_file and self.rtmp) or \
                self.iframe or self.video_mms:
            return True
        return False

    @models.permalink
    def get_absolute_url(self):
        return ('video_item_url', (), {'id':self.id})

    def clean(self):
        r = re.compile("^.*((\.mp4$))", re.IGNORECASE)
        if self.file:
            if not r.findall(os.path.split(self.file.url)[1]):
                raise ValidationError(u"Некорректный тип файла. Вставьте видео формата .mp4")
        if not self.get_params():
            raise ValidationError(u"Необходимо добавить хотя бы один параметр для видео.")

    class Meta:
        verbose_name = u"видео"
        verbose_name_plural = u"видео"

class CategoryAudio(CategoryMedia):
    def is_audio(self): return True
    @models.permalink
    def get_absolute_url(self):
        return ('audio_category_url', (), {'id':self.id})

    class Meta:
        verbose_name = u"категория аудио"
        verbose_name_plural = u"категории аудио"


class AudioItem(Article1Model):
    def make_upload_path(instance, filename):
        return make_file_path(filename, u'upload/media-content/audio/')

    category = models.ForeignKey(CategoryAudio, verbose_name=u'категория', related_name='media_category')
    file = models.FileField(upload_to=make_upload_path, verbose_name=u'файл', blank=True)
    stream = models.CharField(max_length=100, verbose_name=u'ссылка аудио-потока',
                            blank=True,
                            help_text=u'Ссылка вида: http://listen.vedaradio.fm:8000/medium')
    audio_mms = models.CharField(max_length=100, blank=True,
                           verbose_name=u'ссылка для открытия во внешнем проигрывателе',
                           help_text=u'Ссылка вида: mms://195.62.63.238/radio_krishnaloka')

    is_public = models.BooleanField(verbose_name=u'является публичной', default=False)

    objects = models.Manager()
    publics = PublicManager()
    
    def __unicode__(self):
        return self.get_title()

    def get_audio_url(self):
        if self.file:
            return self.file.url
        return False

    def get_audio_params(self):
        if self.file or self.stream or self.audio_mms:
            return True
        return False

    def clean(self):
        r = re.compile("^.*((\.mp3$))", re.IGNORECASE)
        if self.file:
            if not r.findall(os.path.split(self.file.url)[1]):
                raise ValidationError(u"Некорректный тип файла. Вставьте аудио формата .mp3")
        if not self.get_audio_params():
            raise ValidationError(u"Необходимо добавить хотя бы один параметр для аудио.")

    @models.permalink
    def get_absolute_url(self):
        return ('audio_item_url', (), {'id':self.id})


    class Meta:
        verbose_name = u"аудио"
        verbose_name_plural = u"аудио"
