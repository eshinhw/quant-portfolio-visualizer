import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

def sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents):
    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    msg.set_content(contents)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)