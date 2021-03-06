# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 15:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Project', '0006_auto_20170601_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_X',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Slug', models.SlugField(unique=True)),
                ('CompanyName', models.CharField(default='Accenture', max_length=200, verbose_name='Company Name')),
                ('CurrentRole', models.CharField(blank=True, max_length=200, null=True, verbose_name='Current Role')),
                ('User', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='Users',
            field=models.ManyToManyField(blank=True, related_name='Project_Users', to=settings.AUTH_USER_MODEL, verbose_name='Users'),
        ),
    ]
