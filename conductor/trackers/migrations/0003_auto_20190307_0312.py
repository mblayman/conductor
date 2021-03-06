# Generated by Django 2.0.9 on 2019-03-07 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("trackers", "0002_auto_20181025_0210")]

    operations = [
        migrations.AlterField(
            model_name="commonapptracker",
            name="status",
            field=models.PositiveIntegerField(
                choices=[
                    (1, "Pending"),
                    (2, "Tracked"),
                    (3, "International"),
                    (4, "Untracked"),
                    (5, "Removed"),
                    (6, "Parked"),
                ],
                default=1,
            ),
        )
    ]
