# Generated by Django 4.2.7 on 2023-12-07 05:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('FE', '0017_contactmessage_dislikes_contactmessage_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='contactmessage',
            name='likes',
        ),
        migrations.AddField(
            model_name='postform',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postform',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
