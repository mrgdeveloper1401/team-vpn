from django.contrib import admin

from . import models


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['plan_name', "duration", "volume", "price", "max_connect_device", "is_active"]
    list_filter = ['is_active']
    raw_id_fields = ['image']
    list_select_related = ['image']
    list_editable = ['is_active', "max_connect_device"]
    search_fields = ['plan_name']


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_name', "ir_country_name", "is_active"]
    raw_id_fields = ['country_image']
    list_select_related = ['country_image']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['country_name', "ir_country_name"]


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['plan', "country", "is_free", "is_active", "created_at"]
    raw_id_fields = ['plan', "country"]
    list_select_related = ['plan', "country"]
    list_editable = ['is_free', "is_active"]
    list_filter = ['is_free', "is_active"]


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', "is_blocked", "is_active", "created_at"]
    list_editable = ['is_active', "is_blocked"]
    list_filter = ['is_blocked', "is_active"]
    search_fields = ['domain']
