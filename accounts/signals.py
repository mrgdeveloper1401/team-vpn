from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from accounts.models import User

from axes.signals import user_locked_out
from rest_framework.exceptions import PermissionDenied


@receiver(user_locked_out)
def raise_permission_denied(*args, **kwargs):
    raise PermissionDenied("Too many failed login attempts")


@receiver(user_logged_in)
def increase_number_of_login(sender, request, user, **kwargs):
    if isinstance(user, User):
        user.number_of_login += 1
        user.save()
