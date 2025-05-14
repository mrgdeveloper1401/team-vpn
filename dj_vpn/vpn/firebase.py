import firebase_admin
from firebase_admin import credentials, messaging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

firebase_file = BASE_DIR / "vpn69.json"

cred = credentials.Certificate(firebase_file)

firebase_admin.initialize_app(credential=cred)


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
