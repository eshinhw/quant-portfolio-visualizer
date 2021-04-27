import os
import smtplib
import datetime as dt
import pandas_datareader.data as web
from email.message import EmailMessage

def sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents):
    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    msg.set_content(contents)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == '__main__':
    EMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
    EMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
