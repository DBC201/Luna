import argparse
import os
import random
import sqlite3
import sys
import time
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes
from binance.client import Client
from dotenv import load_dotenv

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_scripts.listing_mail import send_mail

DATABASE_PATH = os.path.join(ROOT, "luna_scripts", "listing_mail", "mailing_list.db")
ENV_PATH = os.path.join(ROOT, ".env.local")
load_dotenv(dotenv_path=ENV_PATH)
client = Client(os.environ["api_key"], os.environ["api_secret"])


# https://stackoverflow.com/questions/920910/sending-multipart-html-emails-which-contain-embedded-images
def create_message_with_pics(subject, to, body, image_path):
    msg = EmailMessage()

    # generic email headers
    msg['Subject'] = subject
    msg['From'] = 'lunamonke@gmail.com'
    msg['To'] = to

    # set the plain text body
    msg.set_content(body)

    # now create a Content-ID for the image
    image_cid = make_msgid()
    # if `domain` argument isn't provided, it will
    # use your computer's name

    # set an alternative html body
    msg.add_alternative("""\
        <html>
            <body>
                <p>"""
                        + body +
                        """"</p>
                <img src="cid:{image_cid}">
            </body>
        </html>
        """.format(image_cid=image_cid[1:-1]), subtype='html')
    # image_cid looks like <long.random.number@xyz.com>
    # to use it as the img src, we don't need `<` or `>`
    # so we use [1:-1] to strip them off

    # now open the image and attach it to the email
    with open(image_path, 'rb') as img:
        # know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')

        # attach it
        msg.get_payload()[1].add_related(img.read(),
                                         maintype=maintype,
                                         subtype=subtype,
                                         cid=image_cid)

    # the message is ready now
    # you can write it to a file
    # or send it using smtplib
    return msg


def send_to_all_email_addresses(subject, body, img):
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.cursor()
    cursor.execute('''SELECT email FROM emails WHERE valid = 1''')
    rows = cursor.fetchall()
    for row in rows:
        email = row[0]
        try:
            msg = create_message_with_pics(subject, email, body, img)
            send_mail.send(email, msg.as_string())
        except Exception as e:
            cursor.execute('''UPDATE emails SET valid = ? WHERE email = ?''', [0, email])
            db.commit()
    cursor.close()
    db.close()


def send_bogdanoff(ticker):
    subject = "Dump EET --- " + ticker
    body = "https://www.binance.com/en/trade/" + ticker
    img = "dump/" + random.choice(os.listdir(os.path.join(ROOT, "luna_scripts", "meme", "dump")))
    send_to_all_email_addresses(subject, body, img)


def send_jesse(ticker):
    subject = "Pump EET --- " + ticker
    body = "https://www.binance.com/en/trade/" + ticker
    img = "pump/" + random.choice(os.listdir((os.path.join(ROOT, "luna_scripts", "meme", "pump"))))
    send_to_all_email_addresses(subject, body, img)


def get_vitalik_on_the_line(ticker):
    subject = "Get Vitalik On The Line --- " + ticker
    body = "https://www.binance.com/en/trade/" + ticker
    img = "vitalik/" + random.choice(os.listdir((os.path.join(ROOT, "luna_scripts", "meme", "vitalik"))))
    send_to_all_email_addresses(subject, body, img)


def return_parser():
    parser = argparse.ArgumentParser(description="Send pump dump memes via email")
    parser.add_argument("ticker", type=str, help="Ticker to watch")
    return parser


if __name__ == '__main__':
    args = return_parser().parse_args(sys.argv[1:])
    TICKER = args.ticker.upper()
    initial_price = float(client.get_symbol_ticker(symbol=TICKER)["price"])
    i = 0
    while True:
        price = float(client.get_symbol_ticker(symbol=TICKER)["price"])
        if price < initial_price * 0.9:
            send_bogdanoff(TICKER)
        if price > initial_price * 1.1:
            send_jesse(TICKER)
        if price > initial_price * 1.5:
            get_vitalik_on_the_line(TICKER)
        # update old price every hour
        i += 1
        if ++i % 60 == 0:
            initial_price = price
        time.sleep(60)
