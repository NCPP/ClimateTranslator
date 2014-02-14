# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Job'
        db.create_table(u'ncpp_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Status Unknown', max_length=20)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user', to=orm['auth.User'])),
            ('request', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('response', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('error', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('statusLocation', self.gf('django.db.models.fields.URLField')(max_length=1000, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1000, blank=True)),
            ('submissionDateTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 14, 0, 0), auto_now_add=True, blank=True)),
            ('updateDateTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 14, 0, 0), auto_now=True, blank=True)),
        ))
        db.send_create_signal('ncpp', ['Job'])

        # Adding model 'ClimateIndexJob'
        db.create_table(u'ncpp_climateindexjob', (
            (u'job_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ncpp.Job'], unique=True, primary_key=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('index', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('startDateTime', self.gf('django.db.models.fields.DateField')()),
            ('dataset', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('outputFormat', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('ncpp', ['ClimateIndexJob'])

        # Adding model 'SupportingInfo'
        db.create_table(u'ncpp_supportinginfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ncpp.ClimateIndexJob'])),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('ncpp', ['SupportingInfo'])

        # Adding model 'OpenClimateGisJob'
        db.create_table(u'ncpp_openclimategisjob', (
            (u'job_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ncpp.Job'], unique=True, primary_key=True)),
            ('data_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('time_frequency', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('dataset_category', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('dataset', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('dataset_category2', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('package_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('geometry_category', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('geometry_subcategory', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('geometry_id', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('latmin', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('latmax', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lonmin', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lonmax', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('datetime_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('datetime_stop', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('timeregion_month', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('timeregion_year', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('calc', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('par1', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('par2', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('par3', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('calc_group', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('calc_raw', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('spatial_operation', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('aggregate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('agg_selection', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('output_format', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('prefix', self.gf('django.db.models.fields.CharField')(default='ocgis_output', max_length=50)),
            ('with_auxiliary_files', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ncpp', ['OpenClimateGisJob'])


    def backwards(self, orm):
        # Deleting model 'Job'
        db.delete_table(u'ncpp_job')

        # Deleting model 'ClimateIndexJob'
        db.delete_table(u'ncpp_climateindexjob')

        # Deleting model 'SupportingInfo'
        db.delete_table(u'ncpp_supportinginfo')

        # Deleting model 'OpenClimateGisJob'
        db.delete_table(u'ncpp_openclimategisjob')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ncpp.climateindexjob': {
            'Meta': {'object_name': 'ClimateIndexJob', '_ormbases': ['ncpp.Job']},
            'dataset': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'job_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ncpp.Job']", 'unique': 'True', 'primary_key': 'True'}),
            'outputFormat': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'startDateTime': ('django.db.models.fields.DateField', [], {})
        },
        'ncpp.job': {
            'Meta': {'object_name': 'Job'},
            'error': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Status Unknown'", 'max_length': '20'}),
            'statusLocation': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'blank': 'True'}),
            'submissionDateTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 14, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'updateDateTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 14, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user'", 'to': u"orm['auth.User']"})
        },
        'ncpp.openclimategisjob': {
            'Meta': {'object_name': 'OpenClimateGisJob', '_ormbases': ['ncpp.Job']},
            'agg_selection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'aggregate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'calc': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'calc_group': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'calc_raw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dataset': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dataset_category': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dataset_category2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_stop': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'geometry_category': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'geometry_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'geometry_subcategory': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'job_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ncpp.Job']", 'unique': 'True', 'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'latmax': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'latmin': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lonmax': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lonmin': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'output_format': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'par1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'par2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'par3': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'default': "'ocgis_output'", 'max_length': '50'}),
            'spatial_operation': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time_frequency': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'timeregion_month': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'timeregion_year': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'with_auxiliary_files': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ncpp.supportinginfo': {
            'Meta': {'object_name': 'SupportingInfo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncpp.ClimateIndexJob']"})
        }
    }

    complete_apps = ['ncpp']