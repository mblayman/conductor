# Generated by Django 2.0.6 on 2018-09-09 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("planner", "0021_targetschool_milestones")]

    operations = [
        migrations.AddField(
            model_name="milestone",
            name="semester",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="milestones",
                to="planner.Semester",
            ),
        )
    ]
