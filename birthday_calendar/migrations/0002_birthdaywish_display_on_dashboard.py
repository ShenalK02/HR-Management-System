# Generated by Django 5.2 on 2025-05-03 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("birthday_calendar", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="birthdaywish",
            name="display_on_dashboard",
            field=models.BooleanField(default=True),
        ),
    ]
