from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from rest_framework.exceptions import PermissionDenied
from axes.signals import user_locked_out

from accounts.enums import AccountType, AccountStatus, VolumeChoices
from dj_vpn.accounts.models import User


@receiver(user_locked_out)
def raise_permission_denied(*args, **kwargs):
    raise PermissionDenied("Too many failed login attempts")


@receiver(user_logged_in)
def increase_number_of_login(sender, request, user, **kwargs):
    if isinstance(user, User):
        user.number_of_login += 1
        user.last_login = timezone.now()
        user.save()


# @receiver(post_save, sender=User)
# def check_account_status(sender, instance, created, **kwargs):
#     if instance.start_premium is not None and instance.number_of_days is not None:
#         if instance.volume_choice == VolumeChoices.TRA:
#             if instance.volume < instance.volume_usage / 1_000_000:
#                 instance.account_type = AccountType.normal_user
#                 instance.accounts_status = AccountStatus.LIMIT
#
#         if instance.volume_choice == VolumeChoices.MG:
#             if instance.volume < instance.volume_usage:
#                 instance.account_type = AccountType.normal_user
#                 instance.accounts_status = AccountStatus.LIMIT
#
#         if instance.volume_choice == VolumeChoices.GB:
#             if instance.volume < instance.volume_usage / 1_000:
#                 instance.account_type = AccountType.normal_user
#                 instance.accounts_status = AccountStatus.LIMIT
#         instance.save()
