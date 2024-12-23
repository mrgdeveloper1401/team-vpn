# Generated by Django 5.1.4 on 2024-12-21 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PublicNotification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "is_deleted",
                    models.BooleanField(default=False, editable=False, null=True),
                ),
                ("title", models.CharField(max_length=255)),
                ("body", models.TextField(blank=True, null=True)),
                (
                    "file",
                    models.FileField(blank=True, null=True, upload_to="notifications/"),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "public_notifications",
            },
        ),
        migrations.CreateModel(
            name="UtilsApps",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "is_deleted",
                    models.BooleanField(default=False, editable=False, null=True),
                ),
                ("version_number", models.CharField(max_length=255)),
                (
                    "privacy",
                    models.TextField(blank=True, null=True, verbose_name="حریم خصوصی"),
                ),
            ],
            options={
                "db_table": "utils_apps",
            },
        ),
    ]
