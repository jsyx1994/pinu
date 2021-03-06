# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 01:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FriendShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_each_other', models.BooleanField(default=False)),
                ('level', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('sex', models.CharField(choices=[('M', '\u7537'), ('F', '\u5973')], default='M', max_length=1)),
                ('nick_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('work', models.CharField(blank=True, max_length=20)),
                ('phone_num', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('height', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('weight', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('real_name', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('friends', models.ManyToManyField(related_name='friShip', through='Accounts.FriendShip', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='friendship',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendship',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject', to=settings.AUTH_USER_MODEL),
        ),
    ]
