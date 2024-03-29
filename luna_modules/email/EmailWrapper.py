import mimetypes
import os
import smtplib
import sqlite3
import ssl
from email.message import EmailMessage
from email.utils import make_msgid

current_dir = os.path.dirname(__file__)


class EmailWrapper:
    """Email wrapper for sending emails from database

    See mailing_list.sql for the database schema

    :param port: email port
    :type port: int
    :param smtp_server: smtp link
    :type smtp_server: string
    :param sender_email: sender's email address
    :type sender_mail: string
    :param password: password of the email address
    :type password: string
    :param signature_text: signature text that will appear at the bottom of the email
    :type signature_text: string
    :param database_dir: directory of the database
    :type database_dir: string
    """
    def __init__(self, port, smtp_server, sender_email, password, signature_text,
                 database_dir=os.path.join(current_dir, "mailing_list.db")):
        self.__port = port
        self.__smtp_server = smtp_server
        self.__sender_email = sender_email
        self.__password = password
        self.__signature_text = signature_text
        self.__database_dir = database_dir

    def send_email(self, receiver_email, content):
        """Send an email to given address

        :param receiver_email: address to send to
        :type receiver_email: string
        :param content: raw content of the email
        :type content: string
        :return:
        """
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.__smtp_server, self.__port, context=context) as server:
            server.login(self.__sender_email, self.__password)
            server.sendmail(self.__sender_email, receiver_email, content)

    def clean_database(self):
        """Cleans the invalid email addresses from database

        An address is set to invalid if an error is raised while trying to send

        :return:
        """
        db = sqlite3.connect(self.__database_dir)
        cursor = db.cursor()
        cursor.execute('''DELETE FROM emails WHERE valid = ?''', [0])
        db.commit()
        cursor.close()
        db.close()

    # https://stackoverflow.com/questions/920910/sending-multipart-html-emails-which-contain-embedded-images
    def email_with_picture(self, subject, to, body, image_path):
        """Send multimedia emails

        https://stackoverflow.com/questions/920910/sending-multipart-html-emails-which-contain-embedded-images

        :param subject: subject
        :type subject: string
        :param to: address to send
        :type to: string
        :param body: body content
        :type body: string
        :param image_path: path of the image to be sent
        :type image_path: string
        :return: message object
        :rtype: EmailMessage
        """
        msg = EmailMessage()

        # generic email headers
        msg['Subject'] = subject
        msg['From'] = self.__sender_email
        msg['To'] = to

        # set the plain text body
        msg.set_content(body)

        # now create a Content-ID for the image
        image_cid = make_msgid()
        # if `domain` argument isn't provided, it will
        # use your computer's name

        # set an alternative html body
        msg.add_alternative("""
            <html>
                <body>
                    <p>"""
                            + body +
                            """</p>
                    <img src="cid:{image_cid}">
                    <p>{signature}</p>
                </body>
            </html>
            """.format(signature=self.__signature_text, image_cid=image_cid[1:-1]), subtype='html')
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

    def database_send(self, subject, body, img=None):
        """Send out emails to every address in database

        :param subject: subject of email
        :type subject: string
        :param body: text content for email
        :type body: string
        :param img: path of image to be added
        :type img: string
        :return:
        """
        db = sqlite3.connect(self.__database_dir)
        cursor = db.cursor()
        cursor.execute('''SELECT email FROM emails WHERE valid = 1''')
        rows = cursor.fetchall()
        for row in rows:
            email = row[0]
            try:
                if img:
                    msg = self.email_with_picture(subject, email, body, img)
                    self.send_email(email, msg.as_string())
                else:
                    self.send_email(email, "Subject: " + subject + '\n\n' + body + '\n' + self.__signature_text)
            except FileNotFoundError as e:
                print(e)
            except:
                cursor.execute('''UPDATE emails SET valid = ? WHERE email = ?''', [0, email])
                db.commit()
        cursor.close()
        db.close()
