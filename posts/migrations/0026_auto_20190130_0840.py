# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-30 08:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0025_auto_20190130_0839'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='tweeter',
            new_name='twitter',
        ),
    ]