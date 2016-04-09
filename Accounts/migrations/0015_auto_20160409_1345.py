# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-09 05:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0014_auto_20160408_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='last_login_city',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='myuser',
            name='lat',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='lng',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]