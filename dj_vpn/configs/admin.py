from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin

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
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", 'en_country_name', "fa_country_name", "created_at", "updated_at")
    # raw_id_fields = ['country_image']
    # list_select_related = ['country_image']
    # list_editable = ['is_active']
    # list_filter = ['is_active']
    search_fields = ('en_country_name',)
    list_display_links = ('id', "en_country_name")
    search_help_text = "برای جست و جو میتواند از فیلد (en_country_name) استفاده کنید"
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).defer(
            "is_deleted", "deleted_at"
        )


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "country", "created_at", "config_type", "is_active")
    raw_id_fields = ("country",)
    list_select_related = ("country",)
    list_editable = ("is_active", "config_type")
    list_filter = ("is_active",)
    search_fields = ('country__en_country_name',)
    list_display_links = ("id", "country")
    list_per_page = 20
    search_help_text = "برای جست و جد کردن میتوانید از فیلد (country) استفاده کنید"
    actions = ("activate_selected", "deactivate_selected")

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "country__en_country_name",
            "created_at",
            "updated_at",
            "is_active",
            "config_type",
            "config"
        )

    @admin.action(description="Activate selected configurations")
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected configurations")
    def deactivate_selected(self, request, queryset):
         queryset.update(is_active=False)


# @admin.register(models.Domain)
# class DomainAdmin(admin.ModelAdmin, ImportExportModelAdmin):
#     list_display = ['domain', "is_blocked", "is_active", "created_at"]
#     list_editable = ['is_active', "is_blocked"]
#     list_filter = ['is_blocked', "is_active"]
#     search_fields = ['domain']
