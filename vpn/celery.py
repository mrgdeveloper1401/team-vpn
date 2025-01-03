from celery import Celery

app = Celery('vpn')

app.config_from_object('vpn.celery_config')
app.autodiscover_tasks()

