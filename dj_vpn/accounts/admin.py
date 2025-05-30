from django.contrib import admin
from django.db.models import ExpressionWrapper
from django.db.models import Q, F, IntegerField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from datetime import date
from import_export.admin import ImportExportModelAdmin

from . import forms
from .enums import AccountType
from .models import User, ContentDevice, PrivateNotification, OneDayLeftUser, UserLoginLog


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
        return queryset


class DayLeftZeroFilter(admin.SimpleListFilter):
    title = _("Day left")
    parameter_name = 'day_left'

    def lookups(self, request, model_admin):
        return [
            ("zero", _("zero reminder days")),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'zero':
            return queryset.filter(
                account_type=AccountType.premium_user,
                start_premium__isnull = False,
            ).annotate(
                calcuate_day_left=ExpressionWrapper(
                    date.today() - (F("start_premium") + F("number_of_days")),
                    output_field=IntegerField()
                )
            ).filter(calcuate_day_left=0)


class ContentDeviceInline(admin.TabularInline):
    model = ContentDevice
    extra = 1

    def get_queryset(self, request):
        queryset = super().get_queryset(request).only(
            "user__username", "device_model", "device_os", "device_number", "ip_address",
            "is_blocked"
        )
        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()
        return queryset


@admin.register(User)
class UserAdmin(BaseUserAdmin):
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
                "fields": ("username", "password1", "password2", "volume", "volume_choice",
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
                                         "number_of_max_device", "fcm_token", "user_type", "created_by")}),
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
    inlines = (ContentDeviceInline,)
    list_filter = ('is_active', "is_staff", "is_superuser", "account_type", "accounts_status", NumberOfDaysFilter,
                   "user_type", DayLeftZeroFilter)
    readonly_fields = ("updated_at", "date_joined", "last_login", "all_volume_usage", 'number_of_login')
    list_per_page = 20
    search_fields = ('username',)
    ordering = ('-date_joined',)
    raw_id_fields = ('created_by',)
    search_help_text = _("برای جست و جو میتواندی از یوزرنیم کاربر استفاده کنید")

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
        if not change:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request).defer(
            "is_deleted", "deleted_at"
        )
        if not request.user.is_superuser:
            qs = qs.filter(Q(created_by=request.user) | Q(id=request.user.id))
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            if request.user.has_perm("accounts.change_user"):
                fields_to_disable = (
                    'is_superuser',
                    'is_staff',
                    'is_connected_user',
                    'start_premium',
                    'is_inf_volume',
                    'fcm_token',
                    'user_type',
                    'groups',
                    'user_permissions',
                    "created_by",
                )

                for field_name in fields_to_disable:
                    if field_name in form.base_fields:
                        form.base_fields[field_name].disabled = True
        return form

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj:
                if obj.is_staff and request.user.is_staff:
                    return False
        return super().has_delete_permission(request, obj)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj and obj.id == request.user.id:
            if 'password' in fields:
                del fields['password']
        return fields

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser is False:
            if obj and obj.id == request.user.id:
                return False
        return super().has_change_permission(request, obj)


@admin.register(ContentDevice)
class ContentDeviceAdmin(admin.ModelAdmin):
    list_display = ("id", 'user', "ip_address", "device_model", "is_blocked", "created_at")
    raw_id_fields = ('user',)
    list_select_related = ('user',)
    list_filter = ('is_blocked',)
    list_editable = ('is_blocked',)
    search_fields = ('user__username',)
    ordering = ("-created_at",)
    list_display_links =('id', "user")
    list_per_page = 20
    search_help_text = _("برای جست و جو میتواندی از یوزرنیم کاربر استفاده کنید")
    actions = ("enable_is_block", "disable_is_block")

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "user__username", "device_model", "device_os", "device_number", "ip_address",
            "is_blocked", "created_at", "updated_at"
        )

    @admin.action(description="enable is block")
    def enable_is_block(self, request, queryset):
        print(queryset)
        queryset.update(is_blocked=True)

    @admin.action(description="disable is block")
    def disable_is_block(self, request, queryset):
        queryset.update(is_blocked=False)


@admin.register(PrivateNotification)
class PrivateNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', "title", "created_at")
    list_select_related = ('user',)
    raw_id_fields = ('user',)
    search_fields = ('title', "user__username")
    ordering = ("-created_at",)
    search_help_text = _("برای سرچ کردن میتوانید از فیلد های نام کاربری یوزر و عنوان نوتیفیکیشن استفاده کنید")
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "user__username",
            "title",
            "created_at"
        )


@admin.register(OneDayLeftUser)
class OneDayLeftUserAdmin(admin.ModelAdmin):
    list_display = ("username", "number_of_days", "end_date_subscription", "account_type", "is_staff")
    fieldsets = (
        (None, {
            'fields': (
                'username', "number_of_days", "start_premium"
            ),
        }),
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_per_page = 20
    search_fields = ("username",)
    search_help_text = "برای جست و جو میتواندی از یوزرنیم کاربر استفاده کنید"
    list_filter = ("is_staff",)

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "username",
            "number_of_days",
            "start_premium",
            "account_type",
            "is_staff"
        )


@admin.register(UserLoginLog)
class UserLoginLogAdmin(ImportExportModelAdmin):
    list_display = ("user", "ip_address", "user_agent", "created_at")
    list_select_related = ("user",)
    search_fields = ("user__username",)
    raw_id_fields = ("user",)
    list_per_page = 20
    search_help_text = "برای جست و جو میتواندی از یوزرنیم کاربر استفاده کنید"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "user__username",
            "ip_address",
            "user_agent",
            "created_at"
        )


admin.site.login_form = forms.CustomAdminLoginForm
