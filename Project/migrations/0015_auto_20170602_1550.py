# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0014_extraholidays'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extraholidays',
            name='Start',
            field=models.DateField(verbose_name='Start'),
        ),
    ]
