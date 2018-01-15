# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CategoryFoto'
        db.create_table('media_content_categoryfoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meta_title', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children_category', null=True, to=orm['media_content.CategoryFoto'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('redactor.fields.RedactorField')(max_length=1000)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('media_content', ['CategoryFoto'])

        # Adding model 'FotoItem'
        db.create_table('media_content_fotoitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meta_title', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('text', self.gf('redactor.fields.RedactorField')(max_length=100000)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='media_category', to=orm['media_content.CategoryFoto'])),
            ('file', self.gf('sorl.thumbnail.fields.ImageField')(max_length=500)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('media_content', ['FotoItem'])

        # Adding model 'CategoryVideo'
        db.create_table('media_content_categoryvideo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meta_title', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children_category', null=True, to=orm['media_content.CategoryVideo'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('redactor.fields.RedactorField')(max_length=1000)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('media_content', ['CategoryVideo'])

        # Adding model 'VideoItem'
        db.create_table('media_content_videoitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meta_title', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('text', self.gf('redactor.fields.RedactorField')(max_length=100000)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='media_category', to=orm['media_content.CategoryVideo'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('media_content', ['VideoItem'])

        # Adding model 'CategoryAudio'
        db.create_table('media_content_categoryaudio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meta_title', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children_category', null=True, to=orm['media_content.CategoryAudio'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('redactor.fields.RedactorField')(max_length=1000)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('media_content', ['CategoryAudio'])

        # Adding model 'AudioItem'
        db.create_table('media_content_audioitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meta_title', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('text', self.gf('redactor.fields.RedactorField')(max_length=100000)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='media_category', to=orm['media_content.CategoryAudio'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('media_content', ['AudioItem'])


    def backwards(self, orm):
        # Deleting model 'CategoryFoto'
        db.delete_table('media_content_categoryfoto')

        # Deleting model 'FotoItem'
        db.delete_table('media_content_fotoitem')

        # Deleting model 'CategoryVideo'
        db.delete_table('media_content_categoryvideo')

        # Deleting model 'VideoItem'
        db.delete_table('media_content_videoitem')

        # Deleting model 'CategoryAudio'
        db.delete_table('media_content_categoryaudio')

        # Deleting model 'AudioItem'
        db.delete_table('media_content_audioitem')


    models = {
        'media_content.audioitem': {
            'Meta': {'object_name': 'AudioItem'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media_category'", 'to': "orm['media_content.CategoryAudio']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
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
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
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
        }
    }

    complete_apps = ['media_content']