# Generated by Django 3.2.15 on 2023-02-09 06:05

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('page3', '0027_gameprofile_achievements_gameprofile_additional_info_and_more'),
    ]

    operations = [
        
        migrations.AddField(
            model_name='notifications',
            name='new_likes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='notifications',
            name='new_vouches',
            field=models.CharField(default='', max_length=50, null=True),
        ),
        
    ]
