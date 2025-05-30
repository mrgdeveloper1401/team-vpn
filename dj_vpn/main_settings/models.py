from django.db import models
from django.contrib.postgres.fields import ArrayField

from dj_vpn.accounts.models import User
from dj_vpn.accounts.tasks import send_public_notification
from dj_vpn.cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin
from django.utils.translation import gettext_lazy as _


class PublicNotification(CreateMixin, UpdateMixin, SoftDeleteMixin):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        qs = super().save(*args, **kwargs)
        all_user = User.objects.filter(is_active=True)
        for user in all_user:
            if user.fcm_token:
                send_public_notification(user.fcm_token, qs.title, qs.body)

    class Meta:
        db_table = 'public_notifications'
        ordering = ("-created_at",)


class UtilsApps(CreateMixin, UpdateMixin, SoftDeleteMixin):
    version_number = models.CharField(max_length=255)
    privacy = models.TextField(null=True, blank=True, verbose_name="حریم خصوصی")
    contact_us_phone = ArrayField(
        models.CharField(max_length=20),
        blank=True,
        null=True,
        help_text=_("در این فیلد میتوانید شماره های پشتیبانی خود را وارد کنید. در صورت "
                    "داشتن چندین شماره، بین هر شماره را با کاما جدا کنید.")
    )
    contact_us_email = ArrayField(
        models.EmailField(),
        blank=True,
        null=True,
        help_text=_("در اینجا میتوانید چندین ایمیل پشتیبانی داشته باشید. برای داشتن چندین ایمیل، "
                    "کافی است بین هر ایمیل را با کاما از هم جدا کنید.")
    )
    is_main_settings = models.BooleanField(
        default=True,
        help_text=_("به عنوان تنظیم پیش فرض")
    )

    def __str__(self):
        return self.version_number

    class Meta:
        db_table = 'utils_apps'
        ordering = ("-created_at",)
