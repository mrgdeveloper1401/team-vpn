# Generated by Django 5.1.4 on 2025-01-03 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_remove_contentdevice_last_connected"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="number_of_days",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]