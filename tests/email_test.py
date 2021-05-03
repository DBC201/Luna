import os, sys
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ROOT)
from luna_modules.email.EmailWrapper import EmailWrapper
from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT, ".env.local"))

if __name__ == '__main__':
    emailWrapper = EmailWrapper(
        port=os.environ["ssl_port"],
        smtp_server=os.environ["smtp_server"],
        sender_email=os.environ["email"],
        password=os.environ["email_password"]
    )
    emailWrapper.database_send("test1", "test")
    emailWrapper.database_send("test2", "test", "testImage")
