# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'StudentGroup.sort_key'
        db.add_column(u'grading_studentgroup', 'sort_key',
                      self.gf('django.db.models.fields.CharField')(default='foo', max_length=100),
                      keep_default=False)

        # Adding field 'GradePart.name'
        db.add_column(u'grading_gradepart', 'name',
                      self.gf('django.db.models.fields.CharField')(default='foo', max_length=100),
                      keep_default=False)

        # Adding field 'GradePart.sort_key'
        db.add_column(u'grading_gradepart', 'sort_key',
                      self.gf('django.db.models.fields.CharField')(default='foo', max_length=100),
                      keep_default=False)

        # Adding field 'PartialGrade.short_description'
        db.add_column(u'grading_partialgrade', 'short_description',
                      self.gf('django.db.models.fields.CharField')(default='foo', max_length=100),
                      keep_default=False)

        # Adding field 'PartialGrade.long_description'
        db.add_column(u'grading_partialgrade', 'long_description',
                      self.gf('django.db.models.fields.TextField')(default='foo'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'StudentGroup.sort_key'
        db.delete_column(u'grading_studentgroup', 'sort_key')

        # Deleting field 'GradePart.name'
        db.delete_column(u'grading_gradepart', 'name')

        # Deleting field 'GradePart.sort_key'
        db.delete_column(u'grading_gradepart', 'sort_key')

        # Deleting field 'PartialGrade.short_description'
        db.delete_column(u'grading_partialgrade', 'short_description')

        # Deleting field 'PartialGrade.long_description'
        db.delete_column(u'grading_partialgrade', 'long_description')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'grading.gradeableactivity': {
            'Meta': {'ordering': "('sort_key',)", 'object_name': 'GradeableActivity'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'activities'", 'null': 'True', 'to': u"orm['grading.StudentGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'grading.gradepart': {
            'Meta': {'ordering': "('sort_key',)", 'object_name': 'GradePart'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['grading.GradeableActivity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'required': ('django.db.models.fields.BooleanField', [], {}),
            'sort_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'grading.partialgrade': {
            'Meta': {'object_name': 'PartialGrade'},
            'grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'grade_part': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['grading.GradePart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['grading.Student']"})
        },
        u'grading.student': {
            'Meta': {'object_name': 'Student'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'students'", 'null': 'True', 'to': u"orm['grading.StudentGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'grading.studentgrade': {
            'Meta': {'object_name': 'StudentGrade'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['grading.GradeableActivity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['grading.Student']"})
        },
        u'grading.studentgroup': {
            'Meta': {'ordering': "('sort_key',)", 'object_name': 'StudentGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['grading']