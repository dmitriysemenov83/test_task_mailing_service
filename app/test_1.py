import os
from app.tasks import send_email, send_telegram  # Предполагаем, что функции находятся в tasks.py

# Установите переменные окружения для теста
os.environ['SMTP_HOST'] = 'smtp.yandex.ru'
os.environ['SMTP_PORT'] = '465'
os.environ['SMTP_USER'] = 'damas74@yandex.ru'
os.environ['SMTP_PASSWORD'] = 'thgfgvhgpmifrcyc'
os.environ['SMTP_FROM_EMAIL'] = 'damas74@yandex.ru'
os.environ['TELEGRAM_BOT_TOKEN'] = '6650336705:AAHpYoZk6octkORvKBBI7fCpFohLXsSAhQY'

# SMTP_HOST=smtp.yandex.ru
# SMTP_PORT=465
# SMTP_USER=damas74@yandex.ru
# SMTP_PASSWORD=thgfgvhgpmifrcyc
# #SMTP_FROM_EMAIL=noreply@example.com
# TELEGRAM_BOT_TOKEN=6650336705:AAHpYoZk6octkORvKBBI7fCpFohLXsSAhQY

def test_send_email():
    print("Testing email sending...")
    try:
        send_email('semenov.dmitrii83@gmail.com', 'Дмитрий привет! Не забудь сегодня заехать ко мне!')
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def test_send_telegram():
    print("Testing Telegram message sending...")
    try:
        send_telegram('464136028', 'Дмитрий привет! Не забудь сегодня заехать ко мне!')  # Замените на реальный chat_id
        print("Telegram message sent successfully")
    except Exception as e:
        print(f"Failed to send Telegram message: {str(e)}")

if __name__ == '__main__':
    test_send_email()
    # test_send_telegram()