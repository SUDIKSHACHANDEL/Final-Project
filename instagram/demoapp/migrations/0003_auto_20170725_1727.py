# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 11:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0002_auto_20170725_1727'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='created',
            new_name='created_on',
        ),
    ]
