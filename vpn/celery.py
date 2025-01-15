import os

from celery import Celery
from decouple import config

DEBUG = config("DEBUG", cast=bool)


if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vpn.envs.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vpn.envs.production')

app = Celery('vpn')

app.config_from_object('vpn.celery_config')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
