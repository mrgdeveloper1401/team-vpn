# Generated by Django 5.1.4 on 2024-12-31 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("configs", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Domain",
        ),
        migrations.RemoveField(
            model_name="config",
            name="protocol",
        ),
        migrations.RemoveField(
            model_name="config",
            name="volume",
        ),
    ]
