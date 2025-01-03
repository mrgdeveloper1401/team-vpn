from datetime import timedelta, datetime

from celery import shared_task
from django.db.models import F, ExpressionWrapper, DateTimeField

from accounts.models import User


@shared_task
def change_account_status():
    user_filter = User.objects.filter(
        is_active=True,
        accounts_status='premium_user',
        number_of_days__isnull=False
    )

    end_date = ExpressionWrapper(
        F('start_premium') + timedelta(days=1) * F('number_of_days'),
        output_field=DateTimeField()
    )
    user_filter.filter(end_date__lt=datetime.now()).update(accounts_status='normal_user')
