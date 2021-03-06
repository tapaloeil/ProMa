# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0008_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='name',
            field=models.CharField(default='40', max_length=20, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='friday',
            field=models.DecimalField(decimal_places=2, default='8.0', max_digits=10, verbose_name='Friday'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='monday',
            field=models.DecimalField(decimal_places=2, default='8.0', max_digits=10, verbose_name='Monday'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='saturday',
            field=models.DecimalField(decimal_places=2, default='0.0', max_digits=10, verbose_name='Saturday'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='sunday',
            field=models.DecimalField(decimal_places=2, default='0.0', max_digits=10, verbose_name='Sunday'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='thursday',
            field=models.DecimalField(decimal_places=2, default='8.0', max_digits=10, verbose_name='Thursday'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='tuesday',
            field=models.DecimalField(decimal_places=2, default='8.0', max_digits=10, verbose_name='Tuesday'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='wednesday',
            field=models.DecimalField(decimal_places=2, default='8.0', max_digits=10, verbose_name='Wednesday'),
        ),
    ]
