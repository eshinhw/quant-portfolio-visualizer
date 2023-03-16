import os
import sys
import smtplib
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from email.message import EmailMessage
from credentials import GMAIL_ADDRESS, GMAIL_PW


def sendEmail(recipient_email, balance, investment, performance):
    msg = EmailMessage()
    msg["Subject"] = "Questrade Portfolio Summary"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = recipient_email

    msg.add_alternative(
        f"""\

        <!DOCTYPE html>
        <html>
            <body>
                <p> Hello,<br> Below is the summary of your Questrade portfolio.<br> Have a good day! :) </p>
                <h3> Balance Summary </h3>
                {balance}
                <h3> Performance Summary </h3>
                {performance}
                <h3> Investment Summary </h3>
                {investment}
            </body>
        </html>
    """,
        subtype="html",
    )
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, GMAIL_PW)
        smtp.send_message(msg)
