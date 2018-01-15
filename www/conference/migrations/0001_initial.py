# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ConferenceProfile'
        db.create_table('conference_conferenceprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name=u'conference_profile', unique=True, primary_key=True, to=orm['auth.User'])),
            ('dub_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('one_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('server_email_login', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('server_email_passw', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('conference', ['ConferenceProfile'])

        # Adding model 'Ban'
        db.create_table('conference_ban', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('date_ban_end', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('conference', ['Ban'])

        # Adding model 'Category'
        db.create_table('conference_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('conference', ['Category'])

        # Adding model 'Group'
        db.create_table('conference_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Category'])),
            ('perm', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('redactor.fields.RedactorField')(max_length=10000, blank=True)),
            ('is_visible_members', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_enable_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lifetime', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('conference', ['Group'])

        # Adding M2M table for field leaders on 'Group'
        m2m_table_name = db.shorten_name('conference_group_leaders')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['conference.group'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['group_id', 'user_id'])

        # Adding model 'GroupUserRel'
        db.create_table('conference_groupuserrel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Group'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_frozen', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_ban_end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('conference', ['GroupUserRel'])

        # Adding unique constraint on 'GroupUserRel', fields ['group', 'user']
        db.create_unique('conference_groupuserrel', ['group_id', 'user_id'])

        # Adding model 'Message'
        db.create_table('conference_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(to=orm['conference.Message'], null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Group'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_message_rel', to=orm['auth.User'])),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=10000)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=500, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('conference', ['Message'])

        # Adding model 'MessageRecipientRel'
        db.create_table('conference_messagerecipientrel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_recipient_rel', to=orm['auth.User'])),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='message_recipient_rel', to=orm['conference.Message'])),
            ('is_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_sent_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_removed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('conference', ['MessageRecipientRel'])

        # Adding model 'MessageRequest'
        db.create_table('conference_messagerequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Group'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=10000)),
        ))
        db.send_create_signal('conference', ['MessageRequest'])


    def backwards(self, orm):
        # Removing unique constraint on 'GroupUserRel', fields ['group', 'user']
        db.delete_unique('conference_groupuserrel', ['group_id', 'user_id'])

        # Deleting model 'ConferenceProfile'
        db.delete_table('conference_conferenceprofile')

        # Deleting model 'Ban'
        db.delete_table('conference_ban')

        # Deleting model 'Category'
        db.delete_table('conference_category')

        # Deleting model 'Group'
        db.delete_table('conference_group')

        # Removing M2M table for field leaders on 'Group'
        db.delete_table(db.shorten_name('conference_group_leaders'))

        # Deleting model 'GroupUserRel'
        db.delete_table('conference_groupuserrel')

        # Deleting model 'Message'
        db.delete_table('conference_message')

        # Deleting model 'MessageRecipientRel'
        db.delete_table('conference_messagerecipientrel')

        # Deleting model 'MessageRequest'
        db.delete_table('conference_messagerequest')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'conference.ban': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Ban'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_ban_end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'conference.category': {
            'Meta': {'ordering': "['sort', 'title']", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'conference.conferenceprofile': {
            'Meta': {'object_name': 'ConferenceProfile'},
            'dub_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'one_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'server_email_login': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'server_email_passw': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'conference_profile'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"})
        },
        'conference.group': {
            'Meta': {'ordering': "['sort', 'title']", 'object_name': 'Group'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('redactor.fields.RedactorField', [], {'max_length': '10000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_visible_members': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'leaders': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'leaders_group_rel'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'lifetime': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'perm': ('django.db.models.fields.IntegerField', [], {}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'users_group_rel'", 'blank': 'True', 'through': "orm['conference.GroupUserRel']", 'to': "orm['auth.User']"})
        },
        'conference.groupuserrel': {
            'Meta': {'ordering': "['user__first_name', 'user__last_name', 'user__username']", 'unique_together': "(('group', 'user'),)", 'object_name': 'GroupUserRel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_ban_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_frozen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'conference.message': {
            'Meta': {'ordering': "['id']", 'object_name': 'Message'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['conference.Message']", 'null': 'True', 'blank': 'True'}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'through': "orm['conference.MessageRecipientRel']", 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_message_rel'", 'to': "orm['auth.User']"})
        },
        'conference.messagerecipientrel': {
            'Meta': {'ordering': "['-id']", 'object_name': 'MessageRecipientRel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_sent_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'message_recipient_rel'", 'to': "orm['conference.Message']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_recipient_rel'", 'to': "orm['auth.User']"})
        },
        'conference.messagerequest': {
            'Meta': {'ordering': "['-created']", 'object_name': 'MessageRequest'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['conference']