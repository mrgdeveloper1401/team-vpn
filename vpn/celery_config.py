broker_url = 'redis://localhost:6379/1'
result_backend = 'redis://localhost:6379'
celery_timezone = 'Asia/Tehran'
broker_connection_retry_on_startup = True
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
worker_prefetch_multiplier = 1