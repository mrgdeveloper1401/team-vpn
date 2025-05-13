from datetime import timedelta, date
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.core.exceptions import PermissionDenied, ValidationError

from dj_vpn.cores.managers import UserSoftManager
from dj_vpn.accounts.enums import AccountType, AccountStatus, VolumeChoices
from dj_vpn.accounts.managers import OneDayLeftQuerySet
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
    volume = models.PositiveIntegerField(validators=[MinValueValidator(0)], help_text=_("کاربر چقدر حجم داشته باشد"),
                                         default=0)
    volume_usage = models.FloatField(blank=True, default=0, help_text=_("حجم مصرفی میباشد که بر اساس مگابایت هست"),
                                     validators=[MinValueValidator(0)])
    is_inf_volume = models.BooleanField(default=False, help_text=_("ایا حجم کاربر نامحدود باشد!"))
    all_volume_usage = models.FloatField(default=0, validators=[MinValueValidator(0)], editable=False,
                                         help_text=_("کاربر تا الان چقدر حجم مصرف کرده!"))
    start_premium = models.DateField(blank=True, null=True, help_text=_("تاریخ شروع اشتراک اگر کاربر لاگین کند"
                                                                        " اشتراک کاربر از همان روز شروع خواهد شد"))
    number_of_days = models.PositiveIntegerField(help_text=_("تعداد روز"), null=True, default=0)
    number_of_login = models.PositiveIntegerField(help_text=_("تعداد لاگین های کاربر"), editable=False, db_default=0,
                                                  default=0)
    is_connected_user = models.BooleanField(default=False, help_text=_("این فیلد مشخص میکنه"
                                                                       " که کاربر ایا به کانفیگش متصل شده هست یا خیر"))
    number_of_max_device = models.PositiveIntegerField(default=1,
                                                       help_text=_("هر اکانت چند تا یوزر میتواند به ان متصل شود"))
    fcm_token = models.CharField(max_length=255, blank=True, null=True, help_text=_("fcm token"))
    user_type = models.CharField(
        choices=[("direct", _("مستقیم")), ("tunnel", _("تانل")), ("tunnel_direct", _("تانل و دایرکت"))],
        null=True, blank=True, max_length=14, help_text=_("you can choice --> tunnel - direct - tunnel_direct"))
    created_by = models.ForeignKey('self', related_name="owner", on_delete=models.DO_NOTHING, blank=True,
                                   null=True)
    REQUIRED_FIELDS = ['mobile_phone', "user_type"]

    objects = UserSoftManager()
    # all_objects = AllUserManager()

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
        if self.is_inf_volume:
            return "inf"
        return f'{remaining}, {self.volume_choice}'

    @property
    def day_left(self):
        if self.start_premium is not None and self.number_of_days is not None:
            if self.account_type == AccountType.premium_user:
                reminder_day = (self.end_date_subscription - date.today()).days
                return max(reminder_day, 0)
        return None

    def clean(self):
        if self.volume > 0 and self.is_inf_volume:
            raise ValidationError({"volume": _("volume and is_inf volume they can't be together,"
                                               "you can set volume to 0 and is_inf equal true")})

    def save(self, *args, **kwargs):
        # اگر کاربر لاگین کند برای بار اول تاریخ شروع اکانت مشخص خواهد شد
        if self.number_of_login == 1 and not self.start_premium:
            self.start_premium = date.today()

        if self.start_premium is not None and self.number_of_days is not None:
            if self.volume_choice == VolumeChoices.GB:
                # check if equal
                if self.volume_usage / 1_000 == self.volume:
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.LIMIT
                # check expire data
                elif self.start_premium + timedelta(days=self.number_of_days) < date.today():
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.EXPIRED
                # check premium
                elif self.volume_usage / 1_000 > self.volume:
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.LIMIT
                else:
                    self.account_type = AccountType.premium_user
                    self.accounts_status = AccountStatus.ACTIVE

            if self.volume_choice == VolumeChoices.MG:
                # check equal
                if self.volume_usage == self.volume:
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.LIMIT
                # check datetime
                elif self.start_premium + timedelta(days=self.number_of_days) < date.today():
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.EXPIRED
                # check premium
                elif self.volume_usage > self.volume:
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.LIMIT
                else:
                    self.account_type = AccountType.premium_user
                    self.accounts_status = AccountStatus.ACTIVE

            if self.volume_choice == VolumeChoices.TRA:
                # check equal
                if self.volume_usage / 1_000_000 == self.volume:
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.LIMIT
                # check datetime premium
                elif self.start_premium + timedelta(days=self.number_of_days) < date.today():
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.EXPIRED
                # check premium
                elif self.volume_usage / 1_000_000 > self.volume:
                    self.account_type = AccountType.normal_user
                    self.accounts_status = AccountStatus.LIMIT
                else:
                    self.account_type = AccountType.premium_user
                    self.accounts_status = AccountStatus.ACTIVE

        else:
            self.account_type = AccountType.normal_user
            self.accounts_status = AccountStatus.NOTHING

        if self.is_inf_volume:
            self.accounts_status = AccountStatus.ACTIVE
            self.account_type = AccountType.premium_user

        if self.volume == 0:
            self.account_type = AccountType.normal_user
            self.accounts_status = AccountStatus.NOTHING
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'auth_user'
        ordering = ("-date_joined",)


# one day left user show it
class OneDayLeftUser(User):
    objects = OneDayLeftQuerySet()

    class Meta:
        proxy = True


class ContentDevice(CreateMixin, UpdateMixin, SoftDeleteMixin):
    device_model = models.CharField(max_length=255, help_text=_("مدل دستگاه"), blank=True, null=True)
    device_os = models.CharField(max_length=50, help_text=_("نسخه دستگاه"), blank=True, null=True)
    device_number = models.CharField(max_length=255, help_text=_("سریال گوشی"))
    ip_address = models.GenericIPAddressField(help_text=_("ادرس ای پی"))
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


class PrivateNotification(CreateMixin, UpdateMixin, SoftDeleteMixin):
    title = models.CharField(max_length=255, help_text=_("عنوان اعلانات"))
    body = models.TextField(help_text=_("متن اعلانات"))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, help_text=_("گاربر"))
    is_active = models.BooleanField(default=True, help_text=_("قابل نمایش"))

    def __str__(self):
        return self.title

    def send_to_user(self):
        try:
            send_notification(self.user.fcm_token, self.title, self.body)
        except Exception as e:
            raise ValidationError({"user": e})

    def clean(self):
        if not self.user.fcm_token:
            raise ValidationError({"user": _("User does not have an FCM token.")})
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        self.send_to_user()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'private_notification'
        ordering = ("-created_at",)


class UserLoginLog(CreateMixin):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user_login_log")
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'user_login_log'
