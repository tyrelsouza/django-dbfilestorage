# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-06 19:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbfilestorage', '0009_auto_20170206_1954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dbfile',
            old_name='primary_key',
            new_name='id',
        ),
    ]
