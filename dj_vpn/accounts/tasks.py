from celery import shared_task

from dj_vpn.accounts.models import OneDayLeftUser, User
from dj_vpn.vpn.firebase_conf.firebase import send_notification


@shared_task
def send_notif_one_day_left_user(fcm_token, title, body):
    title = 'اتمام اشتراک شما به زودی'
    body = "شما تنها یک روز از سرویس خود را دارید لطفا اقدام به خرید کنید تا لنگ نمویند"
    all_user = OneDayLeftUser.objects.all()
    for user in all_user:
        send_notification(user.fcm_token, title, body)


@shared_task
def send_public_notification(fcm_token, title, body):
    send_notification(fcm_token, title, body)
