import firebase_admin
from firebase_admin import credentials, messaging
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

firebase_file = os.path.join(BASE_DIR, "team-vpn-702b2-firebase-adminsdk-ykycw-7d32345a5c.json")

cred = credentials.Certificate(firebase_file)

firebase_admin.initialize_app(cred)


def send_notification(token, title, body):
    """ارسال نوتیفیکیشن به یک توکن"""
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    response = messaging.send(message)
    return response
