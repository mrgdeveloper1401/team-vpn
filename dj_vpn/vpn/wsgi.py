"""
WSGI config for vpn project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from decouple import config

debug_mode = config('DEBUG', cast=bool, default=False)

if debug_mode:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vpn.envs.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vpn.envs.production')

application = get_wsgi_application()
