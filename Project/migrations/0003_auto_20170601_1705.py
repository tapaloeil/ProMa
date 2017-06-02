# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 15:05
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0002_auto_20170601_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='Photo',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_image', to='filer.Image'),
        ),
    ]
