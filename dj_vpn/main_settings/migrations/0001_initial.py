# Generated by Django 5.1.8 on 2025-08-01 05:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublicNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_deleted', models.BooleanField(blank=True, editable=False, null=True)),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'public_notifications',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='UtilsApps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_deleted', models.BooleanField(blank=True, editable=False, null=True)),
                ('version_number', models.CharField(max_length=255)),
                ('privacy', models.TextField(blank=True, null=True, verbose_name='حریم خصوصی')),
                ('contact_us_phone', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, help_text='در این فیلد میتوانید شماره های پشتیبانی خود را وارد کنید. در صورت داشتن چندین شماره، بین هر شماره را با کاما جدا کنید.', null=True, size=None)),
                ('contact_us_email', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), blank=True, help_text='در اینجا میتوانید چندین ایمیل پشتیبانی داشته باشید. برای داشتن چندین ایمیل، کافی است بین هر ایمیل را با کاما از هم جدا کنید.', null=True, size=None)),
                ('is_main_settings', models.BooleanField(default=True, help_text='به عنوان تنظیم پیش فرض')),
            ],
            options={
                'db_table': 'utils_apps',
                'ordering': ('-created_at',),
            },
        ),
    ]
