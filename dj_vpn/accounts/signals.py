from django.dispatch import receiver
from rest_framework.exceptions import PermissionDenied
from axes.signals import user_locked_out


@receiver(user_locked_out)
def raise_permission_denied(*args, **kwargs):
    raise PermissionDenied("Too many failed login attempts")
