# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 15:39
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Diaries', '0002_auto_20160327_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
