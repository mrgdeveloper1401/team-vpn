from django.db import models

from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class PublicNotification(CreateMixin, UpdateMixin, SoftDeleteMixin):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    # file = models.FileField(upload_to="notifications/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'public_notifications'


class UtilsApps(CreateMixin, UpdateMixin, SoftDeleteMixin):
    version_number = models.CharField(max_length=255)
    privacy = models.TextField(null=True, blank=True, verbose_name="حریم خصوصی")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.version_number

    class Meta:
        db_table = 'utils_apps'
