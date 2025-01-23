from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from rest_framework.exceptions import PermissionDenied
from axes.signals import user_locked_out

from accounts.models import User


@receiver(user_locked_out)
def raise_permission_denied(*args, **kwargs):
    raise PermissionDenied("Too many failed login attempts")


@receiver(user_logged_in)
def increase_number_of_login(sender, request, user, **kwargs):
    if isinstance(user, User):
        user.number_of_login += 1
        user.last_login = timezone.now()
        user.save()
