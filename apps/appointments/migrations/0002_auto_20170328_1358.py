# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default=b' ', max_length=20),
        ),
    ]
