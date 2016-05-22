# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-17 17:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genomes', '0002_create_dnaslice'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dnaslice',
            unique_together=set([('chromosome', 'start_pos', 'end_pos')]),
        ),
        migrations.AlterIndexTogether(
            name='dnaslice',
            index_together=set([('chromosome', 'start_pos', 'end_pos')]),
        ),
    ]
