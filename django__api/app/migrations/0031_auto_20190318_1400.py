# Generated by Django 2.1.3 on 2019-03-18 14:00

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_auto_20190318_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='recommended_events',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default='[]', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='saved_events',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default='[]', null=True),
        ),
    ]
