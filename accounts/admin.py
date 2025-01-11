from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, AdminUserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User, ContentDevice, PrivateNotification, RecycleUser
from subscriptions.models import UserConfig
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


class NumberOfDaysFilter(admin.SimpleListFilter):
    title = _("Number of days")
    parameter_name = 'number_of_days'

    def lookups(self, request, model_admin):
        return [
            ("false", _("number of days is false"))
        ]

    def queryset(self, request, queryset):
        if self.value() == 'false':
            return queryset.filter(number_of_days__isnull=False)


class ContentDeviceInline(admin.TabularInline):
    model = ContentDevice
    extra = 1


class UserConfigInline(admin.TabularInline):
    model = UserConfig
    extra = 1
    raw_id_fields = ('config',)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "is_connected_user", "is_superuser", "date_joined",
                    "start_premium", "volume", "volume_usage", "account_type", "accounts_status", "number_of_days",
                    "number_of_max_device", "end_date_subscription", "remaining_volume_amount")
    ordering = ('-date_joined',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "volume", "volume_choice",
                           "number_of_days", "start_premium", "number_of_max_device", "account_type", "accounts_status"),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "mobile_phone", "account_type",
                                         "accounts_status", "volume", "volume_usage", "volume_choice",
                                         "number_of_login", "number_of_days",
                                         "number_of_max_device")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_connected_user",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "start_premium", "updated_at")}),
    )
    inlines = [ContentDeviceInline, UserConfigInline]
    list_filter = ['is_active', "is_staff", "is_superuser", "account_type", "accounts_status", NumberOfDaysFilter]
    # list_editable = ['account_type', "accounts_status", "start_premium", 'volume']
    readonly_fields = ['number_of_login', "updated_at"]


@admin.register(ContentDevice)
class ContentDeviceAdmin(ImportExportModelAdmin):
    list_display = ["id", 'user', "ip_address", "device_model", "is_blocked", "created_at"]
    raw_id_fields = ['user']
    list_select_related = ['user']
    list_filter = ['is_blocked']
    list_editable = ['is_blocked']
    search_fields = ['user__username', "ip_address"]
    ordering = ("-created_at",)
    list_display_links = ['id', "user"]


@admin.register(PrivateNotification)
class PrivateNotificationAdmin(ImportExportModelAdmin):
    list_display = ['user', "title", "is_active", "created_at"]
    list_select_related = ['user']
    list_filter = ['is_active']
    raw_id_fields = ['user']
    search_fields = ['title', "user__username"]
    list_editable = ['is_active']
    ordering = ("-created_at",)


@admin.register(RecycleUser)
class RecycleUserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = AdminUserCreationForm
    actions = ['recovery_user']

    @admin.action(description='Recover user')
    def recovery_user(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)
