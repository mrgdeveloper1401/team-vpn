import os
from celery import Celery
from decouple import config
from vpn import settings

DEBUG = config("DEBUG", cast=bool)

if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vpn.envs.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vpn.envs.production')

app = Celery('vpn')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
