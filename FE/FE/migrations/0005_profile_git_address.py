# Generated by Django 4.2.7 on 2023-11-16 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FE', '0004_rename_userprofile_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='git_address',
            field=models.URLField(default='', max_length=30),
        ),
    ]
