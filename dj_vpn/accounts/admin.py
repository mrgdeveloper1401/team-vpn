from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, AdminUserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied

from .models import User, ContentDevice, PrivateNotification, RecycleUser, OneDayLeftUser
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import forms
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


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, BaseUserAdmin):
    add_form = forms.UserAccountCreationForm
    change_password_form = forms.UserAdminPasswordChangeForm
    list_display = ("username", "is_staff", "is_active", "is_connected_user", "start_premium", "volume",
                    "volume_usage", "account_type", "accounts_status", "number_of_days",
                    "day_left", "number_of_max_device", "end_date_subscription", "remaining_volume_amount")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "volume", "volume_choice",
                           "number_of_days", "start_premium", "number_of_max_device", "account_type", "accounts_status",
                           "user_type", "is_inf_volume", "is_staff", "groups", "user_permissions")
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "mobile_phone", "account_type",
                                         "accounts_status", "volume", "volume_usage", "all_volume_usage",
                                         "number_of_login", "number_of_days", "volume_choice", "is_inf_volume",
                                         "number_of_max_device", "fcm_token", "user_type")}),
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
        (_("Important dates"), {"fields": ("last_login", "date_joined", "start_premium", "updated_at", "birth_date")}),
    )
    inlines = [ContentDeviceInline]
    list_filter = ['is_active', "is_staff", "is_superuser", "account_type", "accounts_status", NumberOfDaysFilter]
    readonly_fields = ['number_of_login', "updated_at", "date_joined", "last_login", "all_volume_usage",
                       "account_type", "accounts_status"]
    list_per_page = 20
    search_fields = ['username']
    ordering = ['-date_joined']

    def get_readonly_fields(self, request, obj=None):
        read_only_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            read_only_fields += ["is_superuser", "is_staff", "is_connected_user", "groups", "user_permissions",
                                 "user_type", "is_inf_volume", "start_premium", "fcm_token"]
        return read_only_fields

    def save_model(self, request, obj, form, change):
        if change:
            if not request.user.is_superuser:
                request_user_type = request.user.user_type
                get_user_type = form.cleaned_data.get("user_type")
                if get_user_type != request_user_type:
                    if not request.user.is_superuser:
                        raise PermissionDenied("you not permission this field user_type")
        if obj.id is None:
            if not request.user.is_superuser:
                obj.user_type = request.user.user_type
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user_type=request.user.user_type)
        return qs


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


@admin.register(OneDayLeftUser)
class OneDayLeftUserAdmin(admin.ModelAdmin):
    list_display = ("username", "number_of_days", "end_date_subscription")
    fieldsets = [
        (None, {
            'fields': [
                'username', "number_of_days", "start_premium"
            ],
        }),
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    list_per_page = 20
