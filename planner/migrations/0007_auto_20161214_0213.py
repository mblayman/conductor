# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 02:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0006_auto_20161128_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='matriculation_semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='planner.Semester'),
            preserve_default=False,
        ),
    ]
