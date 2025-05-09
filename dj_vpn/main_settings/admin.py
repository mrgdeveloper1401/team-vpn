from django.contrib import admin

from .models import UtilsApps, PublicNotification
# Register your models here.


@admin.register(UtilsApps)
class UtilsAppsAdmin(admin.ModelAdmin):
    list_display = ['version_number', "is_main_settings", "created_at", "updated_at"]
    list_editable = ['is_main_settings']
    list_filter = ['is_main_settings']


@admin.register(PublicNotification)
class PublicNotificationAdmin(admin.ModelAdmin):
    list_display = ['title', "is_active"]
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['title']
