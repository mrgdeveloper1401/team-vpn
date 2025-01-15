from celery import shared_task

from accounts.models import OneDayLeftUser, User
from vpn.firebase_conf.firebase import send_notification
from main_settings.models import PublicNotification


@shared_task
def send_notif_one_day_left_user(fcm_token, title, body):
    title = 'اتمام اشتراک شما به زودی'
    body = "شما تنها یک روز از سرویس خود را دارید لطفا اقدام به خرید کنید تا لنگ نمویند"
    all_user = OneDayLeftUser.objects.all()
    for user in all_user:
        send_notification(user.fcm_token, title, body)


@shared_task
def send_public_notification(fcm_token, title, body):
    all_user = User.objects.filter(is_active=True)
    last_notification = PublicNotification.objects.last()
    title = last_notification.title
    body = last_notification.body
    for user in all_user:
        if user.fcm_token:
            send_notification(user.fcm_token, title, body)


@shared_task
def add_volume_usage():
    all_user = User.objects.all()
    for user in all_user:
        user.volume_usage += 10
    User.objects.bulk_update(all_user, ['volume_usage'])
