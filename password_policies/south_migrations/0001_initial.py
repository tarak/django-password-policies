# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PasswordChangeRequired'
        db.create_table(u'password_policies_passwordchangerequired', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='password_change_required', unique=True, to=orm['%s.%s' % (User._meta.app_label, User._meta.object_name)])),
        ))
        db.send_create_signal(u'password_policies', ['PasswordChangeRequired'])

        # Adding model 'PasswordHistory'
        db.create_table(u'password_policies_passwordhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='password_history_entries', to=orm['%s.%s' % (User._meta.app_label, User._meta.object_name)])),
        ))
        db.send_create_signal(u'password_policies', ['PasswordHistory'])

    def backwards(self, orm):
        # Deleting model 'PasswordChangeRequired'
        db.delete_table(u'password_policies_passwordchangerequired')

        # Deleting model 'PasswordHistory'
        db.delete_table(u'password_policies_passwordhistory')

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        "%s.%s" % (User._meta.app_label, User._meta.module_name): {
            'Meta': {'object_name': User._meta.module_name, 'db_table': repr(User._meta.db_table)},
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'password_policies.passwordchangerequired': {
            'Meta': {'ordering': "['-created']", 'object_name': 'PasswordChangeRequired'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'password_change_required'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'password_policies.passwordhistory': {
            'Meta': {'ordering': "['-created']", 'object_name': 'PasswordHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'password_history_entries'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['password_policies']
