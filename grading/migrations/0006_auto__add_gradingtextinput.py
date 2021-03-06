# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GradingTextInput'
        db.create_table(u'grading_gradingtextinput', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_input', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('grading', ['GradingTextInput'])


    def backwards(self, orm):
        # Deleting model 'GradingTextInput'
        db.delete_table(u'grading_gradingtextinput')


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
        'grading.autogradeablegradepart': {
            'Meta': {'ordering': "('sort_key',)", 'object_name': 'AutogradeableGradePart', '_ormbases': ['grading.GradePart']},
            'autograding_controller': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'parent': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'autograde'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['grading.GradePart']"})
        },
        'grading.autogradingresult': {
            'Meta': {'ordering': "['save_date']", 'object_name': 'AutogradingResult'},
            'autograder_input_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'autograder_input_pk': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'grade_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradePart']"}),
            'grading_result': ('picklefield.fields.PickledObjectField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'partial_grade': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'autogrades'", 'null': 'True', 'to': "orm['grading.PartialGrade']"}),
            'save_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.Student']"})
        },
        'grading.booleaninput': {
            'Meta': {'object_name': 'BooleanInput'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_input': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'grading.course': {
            'Meta': {'ordering': "('sort_key',)", 'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'grading.gradeableactivity': {
            'Meta': {'ordering': "('sort_key',)", 'object_name': 'GradeableActivity'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'activities'", 'symmetrical': 'False', 'to': "orm['grading.Course']"}),
            'default_grade': ('django.db.models.fields.DecimalField', [], {'default': '2.0', 'max_digits': '5', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'grading.gradepart': {
            'Meta': {'ordering': "('sort_key',)", 'object_name': 'GradePart'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grade_parts'", 'to': "orm['grading.GradeableActivity']"}),
            'default_grade': ('django.db.models.fields.DecimalField', [], {'default': '2.0', 'max_digits': '5', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'passing_grade': ('django.db.models.fields.DecimalField', [], {'default': '3.0', 'max_digits': '5', 'decimal_places': '2'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        'grading.gradingbooleaninput': {
            'Meta': {'object_name': 'GradingBooleanInput'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'required_input': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_input': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'grading.gradingtextinput': {
            'Meta': {'object_name': 'GradingTextInput'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_input': ('django.db.models.fields.TextField', [], {})
        },
        'grading.partialgrade': {
            'Meta': {'ordering': "['save_date']", 'unique_together': "(('student', 'grade_part'),)", 'object_name': 'PartialGrade'},
            'grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'grade_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradePart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'save_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.Student']"})
        },
        'grading.student': {
            'Meta': {'ordering': "('user__last_name', 'user__first_name', 'user__email', 'user__pk')", 'object_name': 'Student'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'students'", 'null': 'True', 'to': "orm['grading.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        'grading.studentgrade': {
            'Meta': {'object_name': 'StudentGrade'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradeableActivity']"}),
            'grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grades'", 'to': "orm['grading.Student']"})
        }
    }

    complete_apps = ['grading']