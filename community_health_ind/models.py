# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models




class County(models.Model):
    county_id = models.IntegerField(primary_key=True)
    county_name = models.CharField(max_length=60, blank=True, null=True)
    location = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'county'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class HealthData(models.Model):
    county = models.ForeignKey(County, models.DO_NOTHING)
    htopic = models.ForeignKey('HealthTopic', models.DO_NOTHING)
    indicator = models.ForeignKey('Indicator', models.DO_NOTHING)
    event_count = models.FloatField(blank=True, null=True)
    avg_num_den = models.FloatField(blank=True, null=True)
    measure = models.CharField(max_length=10, blank=True, null=True)
    percent = models.FloatField(blank=True, null=True)
    mapping_distribution = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'health_data'
        unique_together = (('county', 'htopic', 'indicator'),)


class HealthTopic(models.Model):
    htopic_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'health_topic'


class Indicator(models.Model):
    indicator_id = models.CharField(primary_key=True, max_length=5)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indicator'


class User(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    county = models.IntegerField(blank=True, null=True)
    disease = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'