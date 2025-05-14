import os

from celery import Celery

from decouple import config


DEBUG = config("DEBUG", cast=bool)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_vpn.vpn.envs.development" if DEBUG else "dj_vpn.vpn.envs.production")

celery_app = Celery()

celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.autodiscover_tasks()
