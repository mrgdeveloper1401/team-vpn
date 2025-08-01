# Generated by Django 5.1.8 on 2025-08-01 05:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_deleted', models.BooleanField(blank=True, editable=False, null=True)),
                ('en_country_name', models.CharField(db_index=True, help_text='Names of countries in English', max_length=255)),
                ('fa_country_name', models.CharField(blank=True, help_text='نام کشورها به صورت فارسی', max_length=255, null=True)),
                ('country_code', models.CharField(help_text='کد کشور', max_length=255)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_deleted', models.BooleanField(blank=True, editable=False, null=True)),
                ('config', models.TextField(help_text='کانفینگ')),
                ('config_type', models.CharField(blank=True, choices=[('tunnel', 'سرور تانل'), ('direct', 'سرور مستقیم'), ('tunnel_direct', 'سرور تانل و دایرکت')], max_length=14, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='قابل نمایش')),
                ('country', models.ForeignKey(help_text='کشور مورد نظر', on_delete=django.db.models.deletion.DO_NOTHING, related_name='country_configs', to='configs.country')),
            ],
            options={
                'db_table': 'config',
                'ordering': ('-created_at',),
            },
        ),
    ]
