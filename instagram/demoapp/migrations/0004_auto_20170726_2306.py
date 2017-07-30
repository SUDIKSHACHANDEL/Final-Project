# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 17:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0003_auto_20170725_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentmodel',
            name='post',
        ),
        migrations.RemoveField(
            model_name='commentmodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='likemodel',
            name='post',
        ),
        migrations.RemoveField(
            model_name='likemodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='postmodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='sessiontoken',
            name='user',
        ),
        migrations.DeleteModel(
            name='CommentModel',
        ),
        migrations.DeleteModel(
            name='LikeModel',
        ),
        migrations.DeleteModel(
            name='PostModel',
        ),
        migrations.DeleteModel(
            name='SessionToken',
        ),
    ]