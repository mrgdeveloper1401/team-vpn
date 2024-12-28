from django.contrib.auth.models import AbstractUser
from django.db import models

from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class User(AbstractUser, UpdateMixin, SoftDeleteMixin):
    mobile_phone = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    is_verify = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['mobile_phone']

    class Meta:
        db_table = 'auth_user'
        ordering = ('mobile_phone',)


class ContentDevice(CreateMixin, UpdateMixin, SoftDeleteMixin):
    device_name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    last_connect = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_device')

    def __str__(self):
        return self.device_name

    class Meta:
        db_table = 'content_device'


class RequestLog(CreateMixin, UpdateMixin, SoftDeleteMixin):
    user = models.ForeignKey("accounts.User", on_delete=models.DO_NOTHING, related_name='request_log')
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    logs = models.JSONField()

    class Meta:
        db_table = 'request_log'


class PrivateNotification(CreateMixin, UpdateMixin, SoftDeleteMixin):
    title = models.CharField(max_length=255)
    body = models.TextField()
    file = models.FileField(upload_to="notifications/%Y/%m/%d", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'private_notification'

