# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Student.student_id'
        db.add_column('grading_student', 'student_id',
                      self.gf('django.db.models.fields.CharField')(null=True, max_length=100, unique=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Student.student_id'
        db.delete_column('grading_student', 'student_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'grading.autogradeablegradepart': {
            'Meta': {'_ormbases': ['grading.GradePart'], 'object_name': 'AutogradeableGradePart', 'ordering': "('sort_key',)"},
            'autograding_controller': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'parent': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['grading.GradePart']", 'primary_key': 'True', 'unique': 'True', 'related_name': "'autograde'"})
        },
        'grading.autogradingresult': {
            'Meta': {'object_name': 'AutogradingResult', 'ordering': "['save_date']"},
            'autograder_input_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'autograder_input_pk': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'grade_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradePart']"}),
            'grading_result': ('picklefield.fields.PickledObjectField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'partial_grade': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'autogrades'", 'blank': 'True', 'to': "orm['grading.PartialGrade']", 'null': 'True'}),
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
            'Meta': {'object_name': 'Course', 'ordering': "('sort_key',)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'unique': 'True', 'max_length': '50', 'null': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'})
        },
        'grading.gradeableactivity': {
            'Meta': {'object_name': 'GradeableActivity', 'ordering': "('sort_key',)"},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'activities'", 'to': "orm['grading.Course']", 'symmetrical': 'False'}),
            'default_grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': '2.0', 'max_digits': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'unique': 'True', 'max_length': '50', 'null': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'})
        },
        'grading.gradepart': {
            'Meta': {'object_name': 'GradePart', 'ordering': "('sort_key',)"},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradeableActivity']", 'related_name': "'grade_parts'"}),
            'default_grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': '2.0', 'max_digits': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'passing_grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': '3.0', 'max_digits': '5'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug_field': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'unique': 'True', 'max_length': '50', 'null': 'True'}),
            'sort_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'blank': 'True', 'decimal_places': '2', 'default': '1', 'max_digits': '5'})
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
            'Meta': {'object_name': 'PartialGrade', 'ordering': "['save_date']", 'unique_together': "(('student', 'grade_part'),)"},
            'grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'grade_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradePart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'save_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.Student']"})
        },
        'grading.student': {
            'Meta': {'object_name': 'Student', 'ordering': "('user__last_name', 'user__first_name', 'user__email', 'user__pk')"},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'students'", 'blank': 'True', 'to': "orm['grading.Course']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student_id': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'unique': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'grading.studentgrade': {
            'Meta': {'object_name': 'StudentGrade'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradeableActivity']"}),
            'grade': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.Student']", 'related_name': "'grades'"})
        }
    }

    complete_apps = ['grading']