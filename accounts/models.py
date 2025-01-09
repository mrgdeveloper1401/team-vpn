from datetime import timedelta
from django.utils import timezone
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
    volume_usage = models.FloatField(blank=True, default=0, help_text=_("حجم مصرفی میباشد که بر اساس مگابایت هست"))
    start_premium = models.DateTimeField(blank=True, null=True, help_text=_("تاریخ شروع اشتراک"))
    number_of_days = models.PositiveIntegerField(blank=True, null=True, help_text=_("تعداد روز"))
    number_of_login = models.PositiveIntegerField(help_text=_("تعداد لاگین های کاربر"), editable=False, db_default=0)
    is_connected_user = models.BooleanField(default=False, help_text=_("این فیلد مشخص میکنه"
                                                                       " که کاربر ایا به کانفیگش متصل شده هست یا خیر"))
    number_of_max_device = models.PositiveIntegerField(default=1,
                                                       help_text=_("هر اکانت چند تا یوزر میتواند به ان متصل شود"))

    REQUIRED_FIELDS = ['mobile_phone']

    @property
    def end_date_subscription(self):
        if self.start_premium is not None and self.number_of_days is not None:
            return self.start_premium + timedelta(days=self.number_of_days)
        return None

    def clean(self):
        if self.volume is None:
            raise ValidationError({'volume': _("volume not none")})

    def save(self, *args, **kwargs):
        #   if admin volume_choice == GIG
        if self.volume_choice == VolumeChoices.GB:
            if (self.volume_usage / 1_000) == self.volume or (self.volume_usage / 1_000) > self.volume:
                self.accounts_status = AccountStatus.LIMIT
                self.account_type = AccountType.normal_user
            if self.volume > self.volume_usage / 1_000:
                self.accounts_status = AccountStatus.ACTIVE
                self.account_type = AccountType.premium_user
            if self.end_date_subscription < timezone.now():
                self.accounts_status = AccountStatus.EXPIRED
                self.account_type = AccountType.normal_user
        # if volume_choice == MEG
        elif self.volume_choice == VolumeChoices.MG:
            if self.volume_usage == self.volume or self.volume_usage > self.volume:
                self.accounts_status = AccountStatus.LIMIT
                self.account_type = AccountType.normal_user
            if self.volume > self.volume_usage:
                self.accounts_status = AccountStatus.ACTIVE
                self.account_type = AccountType.premium_user
            if self.end_date_subscription < timezone.now():
                self.accounts_status = AccountStatus.EXPIRED
                self.account_type = AccountType.normal_user
        # if volume_choice = TERA
        else:
            if (self.volume_usage / 1_000_000) == self.volume or (self.volume_usage / 1_000_000) > self.volume:
                self.accounts_status = AccountStatus.LIMIT
                self.account_type = AccountType.normal_user
            if self.volume > self.volume_usage / 1_000_000:
                self.accounts_status = AccountStatus.ACTIVE
                self.account_type = AccountType.premium_user
            if self.end_date_subscription < timezone.now():
                self.accounts_status = AccountStatus.EXPIRED
                self.account_type = AccountType.normal_user
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'auth_user'
        ordering = ("-date_joined",)


class ContentDevice(CreateMixin, UpdateMixin, SoftDeleteMixin):
    device_model = models.CharField(max_length=255, help_text=_("مدل دستگاه"), blank=True, null=True)
    device_os = models.CharField(max_length=50, help_text=_("نسخه دستگاه"), blank=True, null=True)
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
        if self.user.user_device.count() >= self.user.number_of_max_device:
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
