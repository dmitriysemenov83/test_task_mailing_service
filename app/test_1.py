import os
from app.tasks import send_email, send_telegram

# переменные окружения для теста
os.environ['SMTP_HOST'] = 'smtp.yandex.ru'
os.environ['SMTP_PORT'] = '465'
os.environ['SMTP_USER'] = 'mymail@yandex.ru'
os.environ['SMTP_PASSWORD'] = 'smtp_password'
os.environ['SMTP_FROM_EMAIL'] = 'mymail@yandex.ru'
os.environ['TELEGRAM_BOT_TOKEN'] = 'yourtoken'



def test_send_email():
    print("Testing email sending...")
    try:
        send_email('your_mail@mail.com', 'Привет! Это проверка!')
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def test_send_telegram():
    print("Testing Telegram message sending...")
    try:
        send_telegram('you_chat_id', 'Привет! Это проверка!')  # Замените на реальный chat_id
        print("Telegram message sent successfully")
    except Exception as e:
        print(f"Failed to send Telegram message: {str(e)}")

if __name__ == '__main__':
    test_send_email()
    test_send_telegram()