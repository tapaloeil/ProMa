# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 11:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_auto_20170606_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='Owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
