# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-23 21:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("planner", "0003_semester")]

    operations = [
        migrations.RemoveField(model_name="student", name="class_year"),
        migrations.AddField(
            model_name="student",
            name="matriculation_semester",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="planner.Semester",
            ),
        ),
    ]
