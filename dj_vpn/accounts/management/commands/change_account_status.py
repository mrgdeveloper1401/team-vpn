from django.core.management.base import BaseCommand
from django.db.models import F, ExpressionWrapper, DateField
from django.utils import timezone

from dj_vpn.accounts.models import User, AccountType, AccountStatus

class Command(BaseCommand):
    help = "Change account Type for expired subscriptions"

    def handle(self, *args, **options):
        # کاربران پریمیوم که اشتراکشان تمام شده
        expired_users = User.objects.filter(
            account_type=AccountType.premium_user
        ).annotate(
            end_date=ExpressionWrapper(
                F("start_premium") + F("number_of_days"),  # محاسبه تاریخ پایان
                output_field=DateField()
            )
        ).filter(
            end_date__lt=timezone.now()  # تاریخ پایان کوچک‌تر از امروز
        )

        # به‌روزرسانی فیلدها
        updated_count = expired_users.update(
            account_type=AccountType.normal_user,  # تغییر به کاربر معمولی
            accounts_status=AccountStatus.EXPIRED  # وضعیت: منقضی شده
        )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully updated {updated_count} users.")
        )
