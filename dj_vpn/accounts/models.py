from datetime import timedelta, date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.core.exceptions import PermissionDenied

from dj_vpn.accounts.enums import AccountType, AccountStatus, VolumeChoices
from dj_vpn.accounts.managers import DeleteQuerySet, OneDayLeftQuerySet
from dj_vpn.cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin
from dj_vpn.vpn.firebase_conf.firebase import send_notification


class User(AbstractUser, UpdateMixin, SoftDeleteMixin):
    mobile_phone = models.CharField(max_length=15, blank=True, null=True, unique=True,
                                    help_text=_("شماره موبایل کاربر"))
    birth_date = models.DateField(null=True, blank=True, help_text=_("تاریخ تولد"))
    account_type = models.CharField(max_length=15, choices=AccountType.choices, default=AccountType.normal_user,
                                    help_text=_("نوع اکانت"))
    accounts_status = models.CharField(max_length=15, choices=AccountStatus.choices, default=AccountStatus.EXPIRED,
                                       help_text=_("active --> حجم و تاریخ انتقضای کانفینگ کاربر فعال هسنن \n"
                                                   "limit --> لیمیت یعنی کاربر حجمش تموم شده هست \n"
                                                   "expire --> یعنی کاربر روز کانفینگ ان تموم شده هست"))
    volume_choice = models.CharField(max_length=7, choices=VolumeChoices.choices, default=VolumeChoices.GB)
    volume = models.PositiveIntegerField()
    volume_usage = models.FloatField(blank=True, default=0, help_text=_("حجم مصرفی میباشد که بر اساس مگابایت هست"),
                                     validators=[MinValueValidator(0)])
    start_premium = models.DateField(blank=True, null=True, help_text=_("تاریخ شروع اشتراک"))
    number_of_days = models.PositiveIntegerField(help_text=_("تعداد روز"))
    number_of_login = models.PositiveIntegerField(help_text=_("تعداد لاگین های کاربر"), editable=False, db_default=0,
                                                  default=0)
    is_connected_user = models.BooleanField(default=False, help_text=_("این فیلد مشخص میکنه"
                                                                       " که کاربر ایا به کانفیگش متصل شده هست یا خیر"))
    number_of_max_device = models.PositiveIntegerField(default=1,
                                                       help_text=_("هر اکانت چند تا یوزر میتواند به ان متصل شود"))
    fcm_token = models.CharField(max_length=255, blank=True, null=True, help_text=_("fcm token"))
    REQUIRED_FIELDS = ['mobile_phone']

    @property
    def end_date_subscription(self):
        if self.start_premium is not None and self.number_of_days is not None:
            return self.start_premium + timedelta(days=self.number_of_days)
        return None

    @property
    def remaining_volume_amount(self):
        if self.volume_choice == VolumeChoices.GB:
            remaining = self.volume - (self.volume_usage / 1000)
        elif self.volume_choice == VolumeChoices.MG:
            remaining = self.volume - self.volume_usage
        else:
            remaining = self.volume - (self.volume_usage / 1_000_000)
        return f'{remaining}, {self.volume_choice}'

    @property
    def day_left(self):
        if self.account_type == AccountType.premium_user:
            reminder_day = (self.end_date_subscription - date.today()).days
            return max(reminder_day, 0)
        return None

    def save(self, *args, **kwargs):

        if self.number_of_login == 1 and not self.start_premium:
            self.start_premium = date.today()

        if self.start_premium:
            if self.volume_choice == VolumeChoices.GB:
                if self.volume_usage / 1_000 == self.volume:
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.LIMIT
                if self.volume_usage / 1_000 < self.volume and self.number_of_login > 0:
                    self.account_type = AccountType.premium_user
                    self.accounts_status = AccountStatus.ACTIVE
                if self.start_premium + timedelta(days=self.number_of_days) < date.today():
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.EXPIRED

            if self.volume_choice == VolumeChoices.MG:
                if self.volume_usage == self.volume:
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.LIMIT
                if self.volume_usage < self.volume and self.number_of_login > 0:
                    self.account_type = AccountType.premium_user
                    self.accounts_status = AccountStatus.ACTIVE
                if self.start_premium + timedelta(days=self.number_of_days) < date.today():
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.EXPIRED

            if self.volume_choice == VolumeChoices.TRA:
                if self.volume_usage / 1_000_000 == self.volume:
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.LIMIT
                if self.volume_usage / 1_000_000 < self.volume and self.number_of_login > 0:
                    self.account_type = AccountType.premium_user
                    self.accounts_status = AccountStatus.ACTIVE
                if self.start_premium + timedelta(days=self.number_of_days) < date.today():
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.EXPIRED

        else:
            self.account_type = AccountType.normal_user
            self.accounts_status = AccountStatus.NOTHING

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'auth_user'
        ordering = ("-date_joined",)


class RecycleUser(User):
    objects = DeleteQuerySet()

    class Meta:
        proxy = True


class OneDayLeftUser(User):
    objects = OneDayLeftQuerySet()

    class Meta:
        proxy = True


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

    def send_to_user(self):
        try:
            send_notification(self.user.fcm_token, self.title, self.body)
        except Exception as e:
            raise e

    def save(self, *args, **kwargs):
        self.send_to_user()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'private_notification'
        ordering = ("-created_at",)
