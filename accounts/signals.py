from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save
from rest_framework.exceptions import PermissionDenied, ValidationError
from axes.signals import user_locked_out
from rest_framework import status

from accounts.models import User



@receiver(user_locked_out)
def raise_permission_denied(*args, **kwargs):
    raise PermissionDenied("Too many failed login attempts")


@receiver(user_logged_in)
def increase_number_of_login(sender, request, user, **kwargs):
    if isinstance(user, User):
        user.number_of_login += 1
        user.save()


# @receiver(pre_save, sender=User)
# def check_maximum_device(sender, instance, **kwargs):
#     if instance.user_device.count() > instance.number_of_device:
#         raise ValidationError({'detail': "your account max device connection has arrived"},
#                               code=status.HTTP_403_FORBIDDEN)
