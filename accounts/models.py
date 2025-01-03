from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.enums import AccountType, AccountStatus
from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class User(AbstractUser, UpdateMixin, SoftDeleteMixin):
    mobile_phone = models.CharField(max_length=15, blank=True, null=True, unique=True,
                                    help_text=_("شماره موبایل کاربر"))
    birth_date = models.DateField(null=True, blank=True, help_text=_("تاریخ تولد"))
    account_type = models.CharField(max_length=15, choices=AccountType.choices, default=AccountType.normal_user)
    accounts_status = models.CharField(max_length=15, choices=AccountStatus.choices, default=AccountStatus.NOTHING)
    REQUIRED_FIELDS = ['mobile_phone']
    volume = models.PositiveIntegerField(blank=True, null=True)
    volume_usage = models.PositiveIntegerField(blank=True, null=True)
    number_of_days = models.PositiveIntegerField(blank=True, null=True, help_text=_("تعداد روز"))

    class Meta:
        db_table = 'auth_user'


class ContentDevice(CreateMixin, UpdateMixin, SoftDeleteMixin):
    device_model = models.CharField(max_length=255, help_text=_("مدل دستگاه"))
    device_os = models.CharField(max_length=50, help_text=_("نسخه دستگاه"))
    # device_brand = models.CharField(max_length=50, help_text=_("برند گوشی"), blank=True, null=True)
    device_number = models.CharField(max_length=255, help_text=_("سریال گوشی"))
    ip_address = models.GenericIPAddressField(help_text=_("ادرس ای پی"))
    is_connected = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_device',
                             help_text=_("کاربر"))
    is_blocked = models.BooleanField(default=False, help_text=_("بلاک شدن"))

    def __str__(self):
        return f'{self.device_model} {self.device_os} {self.ip_address}'

    class Meta:
        db_table = 'content_device'


# class RequestLog(CreateMixin, UpdateMixin, SoftDeleteMixin):
#     user = models.CharField(editable=False, max_length=255)
#     path = models.CharField(max_length=255, editable=False)
#     method = models.CharField(max_length=10, editable=False)
#     status_code = models.BooleanField(editable=False)
#     template_name = models.CharField(editable=False)
#     logs = models.JSONField(editable=False)
#
#     class Meta:
#         db_table = 'request_log'


class PrivateNotification(CreateMixin, UpdateMixin, SoftDeleteMixin):
    title = models.CharField(max_length=255, help_text=_("عنوان اعلانات"))
    body = models.TextField(help_text=_("متن اعلانات"))
    # file = models.FileField(upload_to="notifications/%Y/%m/%d", null=True, blank=True,
    #                         help_text=_("فایل برای اعلانات"))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, help_text=_("گاربر"))
    is_active = models.BooleanField(default=True, help_text=_("قابل نمایش"))

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'private_notification'
        ordering = ("-created_at",)
