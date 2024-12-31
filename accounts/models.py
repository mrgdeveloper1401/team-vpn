from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class User(AbstractUser, UpdateMixin, SoftDeleteMixin):
    mobile_phone = models.CharField(max_length=15, blank=True, null=True, unique=True,
                                    help_text=_("شماره موبایل کاربر"))
    birth_date = models.DateField(null=True, blank=True, help_text=_("تاریخ تولد"))

    REQUIRED_FIELDS = ['mobile_phone']

    class Meta:
        db_table = 'auth_user'


class ContentDevice(CreateMixin, UpdateMixin, SoftDeleteMixin):
    device_name = models.CharField(max_length=255, help_text=_("نام دستگاه"))
    ip_address = models.GenericIPAddressField(help_text=_("ادرس ای پی"))
    connected_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_device',
                             help_text=_("کاربر"))
    is_blocked = models.BooleanField(default=False, help_text=_("بلاک شدن"))

    def __str__(self):
        return self.device_name

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

