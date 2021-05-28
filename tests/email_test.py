import os, sys
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ROOT)
from luna_modules.email.EmailWrapper import EmailWrapper
from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT, ".env.local"))

if __name__ == '__main__':
    emailWrapper = EmailWrapper(
        port=int(os.environ["ssl_port"]),
        smtp_server=os.environ["smtp_server"],
        sender_email=os.environ["email"],
        password=os.environ["email_password"],
        signature_text="https://bogdanoff.pw"
    )
    emailWrapper.database_send("subject test", "test", "../luna_scripts/meme/pump/pamp-it.gif")
