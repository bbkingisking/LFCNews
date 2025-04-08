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
        recipients = [r.strip() for r in os.getenv("RECIPIENT_EMAIL_ADDRESS").split(",")]

        msg = MIMEMultipart()
        msg['From'] = os.getenv("EMAIL_ADDRESS")
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = "LFC News summary"
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP("smtp.mail.me.com", 587) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            server.sendmail(os.getenv("EMAIL_ADDRESS"), recipients, msg.as_string())

    except Exception as e:
        raise

