import os

from celery import Celery

from decouple import config

<<<<<<< HEAD
DEBUG = config("DEBUG", cast=bool)

settings_module = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_vpn.vpn.envs.production")
=======

DEBUG = config("DEBUG", cast=bool)
>>>>>>> a8216060de05110df38da8ca25c503aa1325822e

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_vpn.vpn.envs.development" if DEBUG else "dj_vpn.vpn.envs.production")

celery_app = Celery()

celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.autodiscover_tasks()
