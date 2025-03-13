from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.db import models

from dj_vpn.cores.managers import SoftManager


# Create your models here.


class CreateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    is_deleted = models.BooleanField(null=True, blank=True, editable=False)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()

    objects = SoftManager()

    class Meta:
        abstract = True
