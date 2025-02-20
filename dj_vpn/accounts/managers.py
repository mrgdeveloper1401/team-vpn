from django.db.models import Manager, F, ExpressionWrapper, DateField
from datetime import date, timedelta

from dj_vpn.accounts.enums import AccountType


class DeleteQuerySet(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class OneDayLeftQuerySet(Manager):
    def get_queryset(self):
        return (super().get_queryset().annotate(
            end_date=ExpressionWrapper(
                F('start_premium') + F('number_of_days'),
                output_field=DateField()
            )
        ).filter(account_type=AccountType.premium_user).
                filter(end_date=date.today() + timedelta(days=1)))
