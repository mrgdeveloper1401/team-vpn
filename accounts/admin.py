from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User, ContentDevice, PrivateNotification
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "date_joined")
    ordering = ('-date_joined',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "mobile_phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@admin.register(ContentDevice)
class ContentDeviceAdmin(ImportExportModelAdmin):
    list_display = ['user', "ip_address", "device_name", "connected_at", "is_blocked", "created_at"]
    raw_id_fields = ['user']
    list_select_related = ['user']
    list_filter = ['is_blocked']
    list_editable = ['is_blocked']
    search_fields = ['user__username', "ip_address"]
    ordering = ("-created_at",)


@admin.register(PrivateNotification)
class PrivateNotificationAdmin(ImportExportModelAdmin):
    list_display = ['user', "title", "is_active", "created_at"]
    list_select_related = ['user']
    list_filter = ['is_active']
    raw_id_fields = ['user']
    search_fields = ['title', "user__username"]
    list_editable = ['is_active']
    ordering = ("-created_at",)
