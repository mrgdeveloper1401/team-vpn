from django.contrib import admin

from .models import User, ContentDevice, PrivateNotification
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    pass


@admin.register(ContentDevice)
class ContentDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', "ip_address", "device_name", "last_connect", "is_active"]
    raw_id_fields = ['user']
    list_select_related = ['user']
    list_filter = ['is_active']
    list_editable = ['is_active']
    search_fields = ['user__username']


@admin.register(PrivateNotification)
class PrivateNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', "title", "is_active"]
    list_select_related = ['user']
    list_filter = ['is_active']
    raw_id_fields = ['user']
    search_fields = ['title', "user__username"]
