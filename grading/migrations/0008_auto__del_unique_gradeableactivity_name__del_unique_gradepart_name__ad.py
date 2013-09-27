# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'GradePart', fields ['name']
        db.delete_unique('grading_gradepart', ['name'])

        # Removing unique constraint on 'GradeableActivity', fields ['name']
        db.delete_unique('grading_gradeableactivity', ['name'])

        # Adding unique constraint on 'GradePart', fields ['activity', 'name']
        db.create_unique('grading_gradepart', ['activity_id', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'GradePart', fields ['activity', 'name']
        db.delete_unique('grading_gradepart', ['activity_id', 'name'])

        # Adding unique constraint on 'GradeableActivity', fields ['name']
        db.create_unique('grading_gradeableactivity', ['name'])

        # Adding unique constraint on 'GradePart', fields ['name']
        db.create_unique('grading_gradepart', ['name'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'grading.autogradeablegradepart': {
            'Meta': {'ordering': "('sort_key',)", 'object_name': 'AutogradeableGradePart', '_ormbases': ['grading.GradePart']},
            'autograding_controller': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'parent': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['grading.GradePart']", 'primary_key': 'True', 'related_name': "'autograde'", 'unique': 'True'})
        },
        'grading.autogradingresult': {
            'Meta': {'ordering': "['save_date']", 'object_name': 'AutogradingResult'},
            'autograder_input_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'autograder_input_pk': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'grade_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradePart']"}),
            'grading_result': ('picklefield.fields.PickledObjectField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'partial_grade': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['grading.PartialGrade']", 'related_name': "'autogrades'", 'null': 'True'}),
            'save_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.Student']"})
        },
        'grading.booleaninput': {
            'Meta': {'object_name': 'BooleanInput'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_input': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'grading.course': {
            'Meta': {'ordering': "('sort_key',)", 'object_name': 'Course'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'null': 'True', 'blank': 'True', 'max_length': '50', 'unique': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'})
        },
        'grading.gradeableactivity': {
            'Meta': {'object_name': 'GradeableActivity'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['grading.Course']", 'symmetrical': 'False', 'related_name': "'activities'"}),
            'default_grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'default': '2.0', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'null': 'True', 'blank': 'True', 'max_length': '50', 'unique': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'})
        },
        'grading.gradepart': {
            'Meta': {'object_name': 'GradePart', 'unique_together': "[('activity', 'name')]"},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradeableActivity']", 'related_name': "'grade_parts'"}),
            'default_grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'default': '2.0', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'passing_grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'default': '3.0', 'decimal_places': '2'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'null': 'True', 'blank': 'True', 'max_length': '50', 'unique': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'blank': 'True', 'default': '1', 'decimal_places': '2', 'max_digits': '5'})
        },
        'grading.gradingbooleaninput': {
            'Meta': {'object_name': 'GradingBooleanInput'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'required_input': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_input': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'grading.gradingtextinput': {
            'Meta': {'object_name': 'GradingTextInput'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_input': ('django.db.models.fields.TextField', [], {})
        },
        'grading.partialgrade': {
            'Meta': {'ordering': "['save_date']", 'object_name': 'PartialGrade', 'unique_together': "(('student', 'grade_part'),)"},
            'grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'grade_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradePart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'save_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.Student']"})
        },
        'grading.student': {
            'Meta': {'ordering': "('user__last_name', 'user__first_name', 'user__email', 'user__pk')", 'object_name': 'Student'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['grading.Course']", 'related_name': "'students'", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student_id': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'unique': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'related_name': "'student'", 'unique': 'True'})
        },
        'grading.studentgrade': {
            'Meta': {'object_name': 'StudentGrade'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradeableActivity']"}),
            'grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.Student']", 'related_name': "'grades'"})
        }
    }

    complete_apps = ['grading']