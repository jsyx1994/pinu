# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-12 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activities', '0016_auto_20160411_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='place',
        ),
        migrations.AddField(
            model_name='activity',
            name='ds_place',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='activity',
            name='st_place',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='activity',
            name='category',
            field=models.CharField(choices=[('SP', '\u8fd0\u52a8'), ('EN', '\u5a31\u4e50'), ('TR', '\u65c5\u884c')], max_length=2),
        ),
    ]