# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ConfigModel'
        db.create_table('configuration_configmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=500)),
        ))
        db.send_create_signal('configuration', ['ConfigModel'])


    def backwards(self, orm):
        # Deleting model 'ConfigModel'
        db.delete_table('configuration_configmodel')


    models = {
        'configuration.configmodel': {
            'Meta': {'object_name': 'ConfigModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '500'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['configuration']