# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GradeableActivity.may_be_autograded_to'
        db.add_column('grading_gradeableactivity', 'may_be_autograded_to',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, default=None, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GradeableActivity.may_be_autograded_to'
        db.delete_column('grading_gradeableactivity', 'may_be_autograded_to')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'grading.autogradeablegradepart': {
            'Meta': {'_ormbases': ['grading.GradePart'], 'object_name': 'AutogradeableGradePart', 'ordering': "('sort_key',)"},
            'autograding_controller': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'may_be_autograded_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'related_name': "'autograde'", 'primary_key': 'True', 'to': "orm['grading.GradePart']"})
        },
        'grading.autogradingresult': {
            'Meta': {'object_name': 'AutogradingResult', 'ordering': "['save_date']"},
            'autograder_input_content_type': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['contenttypes.ContentType']", 'blank': 'True'}),
            'autograder_input_pk': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'grade_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradePart']"}),
            'grading_result': ('picklefield.fields.PickledObjectField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'partial_grade': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'autogrades'", 'to': "orm['grading.PartialGrade']", 'blank': 'True'}),
            'save_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.Student']"})
        },
        'grading.booleaninput': {
            'Meta': {'object_name': 'BooleanInput'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_input': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'grading.course': {
            'Meta': {'object_name': 'Course', 'ordering': "('sort_key',)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '100', 'unique': 'True', 'blank': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'grading.gradeableactivity': {
            'Meta': {'object_name': 'GradeableActivity'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'activities'", 'symmetrical': 'False', 'to': "orm['grading.Course']"}),
            'default_grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': '2.0', 'max_digits': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'may_be_autograded_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '100', 'unique': 'True', 'blank': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'grading.gradepart': {
            'Meta': {'object_name': 'GradePart', 'unique_together': "[('activity', 'name')]", 'ordering': "['sort_key']"},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grade_parts'", 'to': "orm['grading.GradeableActivity']"}),
            'default_grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': 'None', 'max_digits': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'passing_grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': '3.0', 'max_digits': '5'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '100', 'unique': 'True', 'blank': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5', 'default': '1', 'blank': 'True'})
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
            'Meta': {'object_name': 'PartialGrade', 'unique_together': "(('student', 'grade_part'),)", 'ordering': "['save_date']"},
            'grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'grade_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradePart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'save_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.Student']"})
        },
        'grading.student': {
            'Meta': {'object_name': 'Student', 'ordering': "('user__last_name', 'user__first_name', 'user__email', 'user__pk')"},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'students'", 'to': "orm['grading.Course']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student_id': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'unique': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'related_name': "'student'", 'to': "orm['auth.User']"})
        },
        'grading.studentgrade': {
            'Meta': {'object_name': 'StudentGrade'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradeableActivity']"}),
            'grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grades'", 'to': "orm['grading.Student']"})
        }
    }

    complete_apps = ['grading']