# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 13:47
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Project', '0013_auto_20170602_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraHolidays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Start', models.DateField(default=datetime.date.today, verbose_name='Start')),
                ('End', models.DateField(blank=True, null=True, verbose_name='End')),
                ('NbDays', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='Nb Days')),
                ('Status', models.CharField(choices=[('Planned', 'Planned'), ('Registered', 'Registered')], default='Planned', max_length=30)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]