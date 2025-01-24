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


# class Images(CreateMixin, UpdateMixin, SoftDeleteMixin):
#     image = models.ImageField(upload_to='images/%Y/%m/%d', height_field="image_height", width_field="image_width")
#     image_alt = models.CharField(max_length=255, help_text=_("توضیحی برای تصویر خود بگذارید"), blank=True, null=True)
#     image_size = models.PositiveIntegerField(null=True, blank=True)
#     image_width = models.PositiveIntegerField(null=True, blank=True)
#     image_height = models.PositiveIntegerField(null=True, blank=True)
#
#     class Meta:
#         db_table = 'images'
#
#     def save(self, *args, **kwargs):
#         self.image_size = self.image.size
#         return super().save(*args, **kwargs)
