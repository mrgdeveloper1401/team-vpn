# Generated by Django 5.1.4 on 2024-12-21 17:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("configs", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Coupon",
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
                ("coupon_code", models.CharField(max_length=50, unique=True)),
                ("max_used", models.PositiveIntegerField()),
                ("number_of_used", models.PositiveIntegerField(default=0)),
                ("expired_date", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "coupons",
            },
        ),
        migrations.CreateModel(
            name="Discount",
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
                ("is_percent", models.BooleanField(default=False)),
                ("is_value", models.BooleanField(default=False)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="configs.plan"
                    ),
                ),
            ],
            options={
                "db_table": "discounts",
            },
        ),
        migrations.CreateModel(
            name="Subscription",
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
                ("volume_usage", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="plan_subscription",
                        to="configs.plan",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="user_subscription",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "subscriptions",
            },
        ),
    ]