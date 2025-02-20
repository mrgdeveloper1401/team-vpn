from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from . import models


# @admin.register(models.Plan)
# class PlanAdmin(admin.ModelAdmin):
#     list_display = ['plan_name', "duration", "volume", "price", "max_connect_device", "is_active"]
#     list_filter = ['is_active']
#     raw_id_fields = ['image']
#     list_select_related = ['image']
#     list_editable = ['is_active', "max_connect_device"]
#     search_fields = ['plan_name']


@admin.register(models.Country)
class CountryAdmin(ImportExportModelAdmin):
    list_display = ["id", 'en_country_name', "fa_country_name"]
    # raw_id_fields = ['country_image']
    # list_select_related = ['country_image']
    # list_editable = ['is_active']
    # list_filter = ['is_active']
    search_fields = ['en_country_name', "fa_country_name"]
    list_display_links = ['id', "en_country_name"]


@admin.register(models.Config)
class ConfigAdmin(ImportExportModelAdmin):
    list_display = ["country", "created_at", "config_type"]
    raw_id_fields = ["country"]
    list_select_related = ["country"]
    # list_editable = ["is_active"]
    # list_filter = ["is_active"]
    search_fields = ['country__country_name']
    list_editable = ['config_type']


# @admin.register(models.Domain)
# class DomainAdmin(admin.ModelAdmin, ImportExportModelAdmin):
#     list_display = ['domain', "is_blocked", "is_active", "created_at"]
#     list_editable = ['is_active', "is_blocked"]
#     list_filter = ['is_blocked', "is_active"]
#     search_fields = ['domain']
