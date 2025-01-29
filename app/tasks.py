from celery import Celery
from sqlalchemy.orm import sessionmaker
import os
import smtplib
from email.mime.text import MIMEText
import requests
from .models import Message, NotificationLog
from .database import engine


celery = Celery(__name__)
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")

Session = sessionmaker(bind=engine)

@celery.task
def send_notification(message_id: int, recipient: str, recipient_type: str):
    db = Session()
    try:
        message = db.query(Message).get(message_id)
        if not message:
            raise ValueError("Сообщение не найдено")

        status = "success"
        error = None
        try:
            if recipient_type == "email":
                send_email(recipient, message.content)
            elif recipient_type == "telegram":
                send_telegram(recipient, message.content)
        except Exception as e:
            status = "failed"
            error = str(e)
        log = NotificationLog(
            message_id=message_id,
            recipient=recipient,
            recipient_type=recipient_type,
            status=status,
            error_message=error
        )
        db.add(log)
        db.commit()
    finally:
        db.close()


def send_email(to: str, content: str):
    msg = MIMEText(content)
    msg["Subject"] = "Notification"
    msg["From"] = os.getenv("SMTP_FROM_EMAIL")
    msg["To"] = to

    with smtplib.SMTP_SSL(
        os.getenv("SMTP_HOST"),
        int(os.getenv("SMTP_PORT"))
    ) as server:
        server.login(
            os.getenv("SMTP_USER"),
            os.getenv("SMTP_PASSWORD")
        )
        server.send_message(msg)

def send_telegram(chat_id: str, content: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, json={
        "chat_id": chat_id,
        "text": content
    })
    response.raise_for_status()