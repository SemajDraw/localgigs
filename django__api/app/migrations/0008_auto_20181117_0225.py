# Generated by Django 2.1.3 on 2018-11-17 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20181117_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='static/user/profile_pic/default_profile.jpeg', upload_to='static/user/profile_pic/'),
        ),
    ]
