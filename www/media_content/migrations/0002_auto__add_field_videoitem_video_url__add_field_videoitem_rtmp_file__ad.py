# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'VideoItem.video_url'
        db.add_column('media_content_videoitem', 'video_url',
                      self.gf('embed_video.fields.EmbedVideoField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'VideoItem.rtmp_file'
        db.add_column('media_content_videoitem', 'rtmp_file',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'VideoItem.rtmp'
        db.add_column('media_content_videoitem', 'rtmp',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'VideoItem.iframe'
        db.add_column('media_content_videoitem', 'iframe',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True),
                      keep_default=False)

        # Adding field 'VideoItem.video_mms'
        db.add_column('media_content_videoitem', 'video_mms',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'AudioItem.stream'
        db.add_column('media_content_audioitem', 'stream',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'AudioItem.audio_mms'
        db.add_column('media_content_audioitem', 'audio_mms',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'VideoItem.video_url'
        db.delete_column('media_content_videoitem', 'video_url')

        # Deleting field 'VideoItem.rtmp_file'
        db.delete_column('media_content_videoitem', 'rtmp_file')

        # Deleting field 'VideoItem.rtmp'
        db.delete_column('media_content_videoitem', 'rtmp')

        # Deleting field 'VideoItem.iframe'
        db.delete_column('media_content_videoitem', 'iframe')

        # Deleting field 'VideoItem.video_mms'
        db.delete_column('media_content_videoitem', 'video_mms')

        # Deleting field 'AudioItem.stream'
        db.delete_column('media_content_audioitem', 'stream')

        # Deleting field 'AudioItem.audio_mms'
        db.delete_column('media_content_audioitem', 'audio_mms')


    models = {
        'media_content.audioitem': {
            'Meta': {'object_name': 'AudioItem'},
            'audio_mms': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media_category'", 'to': "orm['media_content.CategoryAudio']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'stream': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('redactor.fields.RedactorField', [], {'max_length': '100000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'media_content.categoryaudio': {
            'Meta': {'object_name': 'CategoryAudio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children_category'", 'null': 'True', 'to': "orm['media_content.CategoryAudio']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'text': ('redactor.fields.RedactorField', [], {'max_length': '1000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'media_content.categoryfoto': {
            'Meta': {'object_name': 'CategoryFoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children_category'", 'null': 'True', 'to': "orm['media_content.CategoryFoto']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'text': ('redactor.fields.RedactorField', [], {'max_length': '1000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'media_content.categoryvideo': {
            'Meta': {'object_name': 'CategoryVideo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children_category'", 'null': 'True', 'to': "orm['media_content.CategoryVideo']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'text': ('redactor.fields.RedactorField', [], {'max_length': '1000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'media_content.fotoitem': {
            'Meta': {'object_name': 'FotoItem'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media_category'", 'to': "orm['media_content.CategoryFoto']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'text': ('redactor.fields.RedactorField', [], {'max_length': '100000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'media_content.videoitem': {
            'Meta': {'object_name': 'VideoItem'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media_category'", 'to': "orm['media_content.CategoryVideo']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iframe': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rtmp': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'rtmp_file': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'text': ('redactor.fields.RedactorField', [], {'max_length': '100000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'video_mms': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'video_url': ('embed_video.fields.EmbedVideoField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['media_content']