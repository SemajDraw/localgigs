# Generated by Django 2.1.3 on 2019-03-07 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_spotify_user_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spotify',
            old_name='artists',
            new_name='artist_count',
        ),
        migrations.RemoveField(
            model_name='spotify',
            name='playlist_IDs',
        ),
    ]
