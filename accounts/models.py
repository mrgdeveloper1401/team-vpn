from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError
from django.core.exceptions import PermissionDenied

from accounts.enums import AccountType, AccountStatus, VolumeChoices
from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class User(AbstractUser, UpdateMixin, SoftDeleteMixin):
    mobile_phone = models.CharField(max_length=15, blank=True, null=True, unique=True,
                                    help_text=_("شماره موبایل کاربر"))
    birth_date = models.DateField(null=True, blank=True, help_text=_("تاریخ تولد"))
    account_type = models.CharField(max_length=15, choices=AccountType.choices, default=AccountType.normal_user,
                                    help_text=_("نوع اکانت"))
    accounts_status = models.CharField(max_length=15, choices=AccountStatus.choices, default=AccountStatus.NOTHING,
                                       help_text=_("active --> حجم و تاریخ انتقضای کانفینگ کاربر فعال هسنن \n"
                                                   "limit --> لیمیت یعنی کاربر حجمش تموم شده هست \n"
                                                   "expire --> یعنی کاربر روز کانفینگ ان تموم شده هست"))
    volume_choice = models.CharField(max_length=7, choices=VolumeChoices.choices, default=VolumeChoices.GB)
    volume = models.PositiveIntegerField(blank=True, default=0)
    volume_usage = models.FloatField(blank=True, default=0)
    start_premium = models.DateTimeField(blank=True, null=True, help_text=_("تاریخ شروع اشتراک"))
    number_of_days = models.PositiveIntegerField(blank=True, null=True, help_text=_("تعداد روز"))
    number_of_login = models.PositiveIntegerField(help_text=_("تعداد لاگین های کاربر"), editable=False, db_default=0)
    is_connected_user = models.BooleanField(default=False, help_text=_("این فیلد مشخص میکنه"
                                                                       " که کاربر ایا به کانفیگش متصل شده هست یا خیر"))
    number_of_device = models.PositiveIntegerField(default=1, help_text=_("هر اکانت چند تا یوزر میتواند به ان متصل شود"))

    REQUIRED_FIELDS = ['mobile_phone']

    def clean(self):
        if self.volume is None:
            raise ValidationError({'volume': _("volume not none")})

    def save(self, *args, **kwargs):
        if self.volume >= 1:
            self.accounts_status = AccountStatus.ACTIVE
            self.account_type = AccountType.premium_user
        if self.volume_usage == self.volume:
            self.accounts_status = AccountStatus.LIMIT
            self.volume = 0
            self.volume_usage = 0
            self.account_type = AccountType.normal_user
            self.start_premium = None
            self.number_of_days = 0
        if self.number_of_days == 0:
            self.volume = 0
            self.volume_usage = 0
            self.account_type = AccountType.normal_user
            self.start_premium = None
            self.accounts_status = AccountStatus.EXPIRED
        if self.pk is None:
            self.accounts_status = AccountStatus.NOTHING
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'auth_user'
        ordering = ("-date_joined",)


class ContentDevice(CreateMixin, UpdateMixin, SoftDeleteMixin):
    device_model = models.CharField(max_length=255, help_text=_("مدل دستگاه"))
    device_os = models.CharField(max_length=50, help_text=_("نسخه دستگاه"))
    # device_brand = models.CharField(max_length=50, help_text=_("برند گوشی"), blank=True, null=True)
    device_number = models.CharField(max_length=255, help_text=_("سریال گوشی"))
    ip_address = models.GenericIPAddressField(help_text=_("ادرس ای پی"))
    # is_connected = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_device',
                             help_text=_("کاربر"))
    is_blocked = models.BooleanField(default=False, help_text=_("بلاک شدن"))

    def __str__(self):
        return f'{self.device_model} {self.device_os} {self.ip_address}'

    def save(self, *args, **kwargs):
        if self.user.user_device.count() >= self.user.number_of_device:
            if not self.pk:
                raise PermissionDenied('your account max device connection has arrived')
        return super().save(*args, **kwargs)

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
