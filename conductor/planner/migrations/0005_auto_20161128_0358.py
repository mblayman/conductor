# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-28 03:58
from __future__ import unicode_literals
import datetime

from django.db import migrations


def initial_semesters(apps, schema_editor):
    Semester = apps.get_model("planner", "Semester")
    Semester.objects.create(date=datetime.date(2018, 11, 1))
    Semester.objects.create(date=datetime.date(2019, 4, 1))
    Semester.objects.create(date=datetime.date(2019, 7, 1))


class Migration(migrations.Migration):

    dependencies = [("planner", "0004_auto_20161123_2102")]

    operations = [migrations.RunPython(initial_semesters)]
