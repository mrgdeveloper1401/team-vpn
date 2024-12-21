from django.db.models import QuerySet, Manager
from django.utils import timezone


class SoftQuerySet(QuerySet):
    def delete(self):
        super().update(is_deleted=True, deleted_at=timezone.now())


class SoftManager(Manager):
    def get_queryset(self):
        return SoftQuerySet(self.model, using=self._db).filter(is_deleted=False, is_deleted_at=None)
