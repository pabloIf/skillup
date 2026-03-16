import smtplib, os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "vovabandit2010@gmail.com"
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

def send_reactivate_email(user_email: str, token: str):
    link = f"http://127.0.0.1:8000/users/reactivate?token={token}"
    body = f"Натисніть на посилання, щоб активувати акаунт: {link}"
    send_email(user_email, "Reactivate your account", body)