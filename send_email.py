# send_email.py 

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()

def send_email(message):
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv("EMAIL_ADDRESS")
        msg['To'] = os.getenv("RECIPIENT_EMAIL_ADDRESS")
        msg['Subject'] = "LFC News summary"
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP("smtp.mail.me.com", 587) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)

    except Exception as e:
        raise
