import smtplib
import ssl
import os
from dotenv import load_dotenv


def send(receiver_email, message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    load_dotenv(dotenv_path="../../.env.local")
    sender_email = os.environ["email"]
    password = os.environ["email_password"]

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
