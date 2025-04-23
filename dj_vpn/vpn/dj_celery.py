import os

from celery import Celery

from decouple import config

DEBUG = config("DEBUG", cast=bool)

settings_module = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_vpn.vpn.envs.production")


celery_app = Celery("vpn")

celery_app.config_from_object(settings_module)

celery_app.conf.update(
    timezone="Asia/Tehran",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    worker_prefetch_multiplier=1,
    result_expires=120,
    task_always_eager=False,
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
)

celery_app.autodiscover_tasks()


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
