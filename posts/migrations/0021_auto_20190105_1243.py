# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-01-05 12:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_auto_20190105_1233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='otherusers',
            new_name='Following',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='current_user',
            new_name='user',
        ),
    ]