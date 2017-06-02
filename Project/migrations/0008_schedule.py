# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0007_auto_20170601_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday', models.DecimalField(decimal_places=2, default='8.0', max_digits=10)),
                ('tuesday', models.DecimalField(decimal_places=2, default='8.0', max_digits=10)),
                ('wednesday', models.DecimalField(decimal_places=2, default='8.0', max_digits=10)),
                ('thursday', models.DecimalField(decimal_places=2, default='8.0', max_digits=10)),
                ('friday', models.DecimalField(decimal_places=2, default='8.0', max_digits=10)),
                ('saturday', models.DecimalField(decimal_places=2, default='0.0', max_digits=10)),
                ('sunday', models.DecimalField(decimal_places=2, default='0.0', max_digits=10)),
            ],
        ),
    ]
