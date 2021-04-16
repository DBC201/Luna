import smtplib
import ssl
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../../.env.local")


def send(receiver_email, message):
    port = os.environ["ssl_port"]
    smtp_server = os.environ["smtp_server"]
    sender_email = os.environ["email"]
    password = os.environ["email_password"]

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
