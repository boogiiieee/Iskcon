# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ConfigModel.email_sign'
        db.add_column('configuration_configmodel', 'email_sign',
                      self.gf('redactor.fields.RedactorField')(default='', max_length=1000, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ConfigModel.email_sign'
        db.delete_column('configuration_configmodel', 'email_sign')


    models = {
        'configuration.configmodel': {
            'Meta': {'object_name': 'ConfigModel'},
            'email_sign': ('redactor.fields.RedactorField', [], {'max_length': '1000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '500'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['configuration']