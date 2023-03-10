# Generated by Django 3.2.15 on 2023-02-09 07:08

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('page3', '0028_auto_20230209_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='new_likes',
        ),
        migrations.AddField(
            model_name='notifications',
            name='new_likes',
            field=models.ManyToManyField(blank=True, default=None, related_name='new_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='new_vouches',
        ),
        migrations.AddField(
            model_name='notifications',
            name='new_vouches',
            field=models.ManyToManyField(blank=True, default=None, related_name='new_vouches', to=settings.AUTH_USER_MODEL),
        ),
        
    ]
