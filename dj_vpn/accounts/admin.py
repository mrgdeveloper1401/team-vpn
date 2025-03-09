from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, AdminUserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
# from guardian.admin import GuardedModelAdmin
# from guardian.shortcuts import get_objects_for_user

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
    readonly_fields = ["updated_at", "date_joined", "last_login", "account_type", "accounts_status",
                       "all_volume_usage", 'number_of_login']
    list_per_page = 20
    search_fields = ['username']
    ordering = ['-date_joined']

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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            if request.user.has_perm("accounts.change_user"):
                form.base_fields['is_superuser'].disabled = True
                form.base_fields['is_staff'].disabled = True
                form.base_fields['is_connected_user'].disabled = True
                form.base_fields['start_premium'].disabled = True
                form.base_fields['is_inf_volume'].disabled = True
                form.base_fields['fcm_token'].disabled = True
                form.base_fields['user_type'].disabled = True
                form.base_fields['groups'].disabled = True
                form.base_fields['user_permissions'].disabled = True
        return form

    # def has_module_permission(self, request):
    #     is_superuser = request.user.is_superuser
    #     if is_superuser:
    #         return True
    #     return self.get_model_objects(request).exists()

    # def get_model_objects(self, request, action=None, klass=None):
    #     opts = self.opts
    #     actions = [action] if action else ['view', "edit", "delete"]
    #     klass = klass if klass else opts.model
    #     model_name = klass._meta.model_name
    #     return get_objects_for_user(user=request.user, perms=[f"{perm}_{model_name}" for perm in actions], klass=klass,
    #                                 any_perm=True)

    # def has_permissions(self, request, obj, action):
    #     opts = self.opts
    #     code_name = f'{action}_{opts.model_name}'
    #     if obj:
    #         return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
    #     else:
    #         return self.get_model_objects(request).exists()

    # def has_view_permission(self, request, obj=None):
    #     return self.has_permissions(request, obj, "view")

    # def has_change_permission(self, request, obj=None):
    #     return self.has_permissions(request, obj, "change")

    # def has_delete_permission(self, request, obj=None):
    #     return self.has_permissions(request, obj, "delete")


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
