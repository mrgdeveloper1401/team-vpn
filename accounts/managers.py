from django.db.models import Manager, QuerySet


class DeleteQuerySet(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)
