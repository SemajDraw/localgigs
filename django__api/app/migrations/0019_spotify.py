# Generated by Django 2.1.3 on 2019-02-22 22:06

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0018_delete_spotify'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spotify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField(blank=True, max_length=500, null=True)),
                ('artists', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
