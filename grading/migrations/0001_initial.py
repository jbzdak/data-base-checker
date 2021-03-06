# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GradingBooleanInput'
        db.create_table(u'grading_gradingbooleaninput', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_input', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('required_input', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('grading', ['GradingBooleanInput'])

        # Adding model 'BooleanInput'
        db.create_table(u'grading_booleaninput', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_input', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('grading', ['BooleanInput'])

        # Adding model 'Student'
        db.create_table(u'grading_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='students', null=True, to=orm['grading.Course'])),
        ))
        db.send_create_signal('grading', ['Student'])

        # Adding model 'Course'
        db.create_table(u'grading_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('sort_key', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('grading', ['Course'])

        # Adding model 'GradeableActivity'
        db.create_table(u'grading_gradeableactivity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('sort_key', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('default_grade', self.gf('django.db.models.fields.DecimalField')(default=2.0, max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('grading', ['GradeableActivity'])

        # Adding M2M table for field courses on 'GradeableActivity'
        m2m_table_name = db.shorten_name(u'grading_gradeableactivity_courses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gradeableactivity', models.ForeignKey(orm['grading.gradeableactivity'], null=False)),
            ('course', models.ForeignKey(orm['grading.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gradeableactivity_id', 'course_id'])

        # Adding model 'GradePart'
        db.create_table(u'grading_gradepart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('sort_key', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=5, decimal_places=2, blank=True)),
            ('default_grade', self.gf('django.db.models.fields.DecimalField')(default=2.0, max_digits=5, decimal_places=2)),
            ('passing_grade', self.gf('django.db.models.fields.DecimalField')(default=3.0, max_digits=5, decimal_places=2)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='grade_parts', to=orm['grading.GradeableActivity'])),
        ))
        db.send_create_signal('grading', ['GradePart'])

        # Adding model 'PartialGrade'
        db.create_table(u'grading_partialgrade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grade', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['grading.Student'])),
            ('grade_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['grading.GradePart'])),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('grading', ['PartialGrade'])

        # Adding unique constraint on 'PartialGrade', fields ['student', 'grade_part']
        db.create_unique(u'grading_partialgrade', ['student_id', 'grade_part_id'])

        # Adding model 'AutogradingResult'
        db.create_table(u'grading_autogradingresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grade', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['grading.Student'])),
            ('grade_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['grading.GradePart'])),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('autograder_input_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('autograder_input_pk', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('grading_result', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('grading', ['AutogradingResult'])

        # Adding unique constraint on 'AutogradingResult', fields ['student', 'grade_part']
        db.create_unique(u'grading_autogradingresult', ['student_id', 'grade_part_id'])

        # Adding model 'AutogradeableGradePart'
        db.create_table(u'grading_autogradeablegradepart', (
            ('parent', self.gf('django.db.models.fields.related.OneToOneField')(related_name='bdchecker_part', unique=True, primary_key=True, to=orm['grading.GradePart'])),
            ('autograding_controller', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('grading', ['AutogradeableGradePart'])

        # Adding model 'StudentGrade'
        db.create_table(u'grading_studentgrade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='grades', to=orm['grading.Student'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['grading.GradeableActivity'])),
            ('grade', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('grading', ['StudentGrade'])


    def backwards(self, orm):
        # Removing unique constraint on 'AutogradingResult', fields ['student', 'grade_part']
        db.delete_unique(u'grading_autogradingresult', ['student_id', 'grade_part_id'])

        # Removing unique constraint on 'PartialGrade', fields ['student', 'grade_part']
        db.delete_unique(u'grading_partialgrade', ['student_id', 'grade_part_id'])

        # Deleting model 'GradingBooleanInput'
        db.delete_table(u'grading_gradingbooleaninput')

        # Deleting model 'BooleanInput'
        db.delete_table(u'grading_booleaninput')

        # Deleting model 'Student'
        db.delete_table(u'grading_student')

        # Deleting model 'Course'
        db.delete_table(u'grading_course')

        # Deleting model 'GradeableActivity'
        db.delete_table(u'grading_gradeableactivity')

        # Removing M2M table for field courses on 'GradeableActivity'
        db.delete_table(db.shorten_name(u'grading_gradeableactivity_courses'))

        # Deleting model 'GradePart'
        db.delete_table(u'grading_gradepart')

        # Deleting model 'PartialGrade'
        db.delete_table(u'grading_partialgrade')

        # Deleting model 'AutogradingResult'
        db.delete_table(u'grading_autogradingresult')

        # Deleting model 'AutogradeableGradePart'
        db.delete_table(u'grading_autogradeablegradepart')

        # Deleting model 'StudentGrade'
        db.delete_table(u'grading_studentgrade')


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
            'parent': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'bdchecker_part'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['grading.GradePart']"})
        },
        'grading.autogradingresult': {
            'Meta': {'unique_together': "(('student', 'grade_part'),)", 'object_name': 'AutogradingResult'},
            'autograder_input_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'autograder_input_pk': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'grade_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradePart']"}),
            'grading_result': ('picklefield.fields.PickledObjectField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'sort_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'grading.gradeableactivity': {
            'Meta': {'ordering': "('sort_key',)", 'object_name': 'GradeableActivity'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'activities'", 'symmetrical': 'False', 'to': "orm['grading.Course']"}),
            'default_grade': ('django.db.models.fields.DecimalField', [], {'default': '2.0', 'max_digits': '5', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
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
            'sort_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        'grading.gradingbooleaninput': {
            'Meta': {'object_name': 'GradingBooleanInput'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'required_input': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_input': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'grading.partialgrade': {
            'Meta': {'unique_together': "(('student', 'grade_part'),)", 'object_name': 'PartialGrade'},
            'grade': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'grade_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grading.GradePart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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