# Generated by Django 4.0.6 on 2023-01-09 08:10

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page3', '0005_gameprofile_achievements_gameprofile_additional_info_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameprofile',
            old_name='server',
            new_name='region',
        ),
        migrations.AddField(
            model_name='gameprofile',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='gameprofile',
            name='servers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='', max_length=50, null=True), blank=True, default=list, null=True, size=None),
        ),
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.IntegerField(null=True),
        ),
    ]
