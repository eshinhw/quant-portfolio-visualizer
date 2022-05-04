import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "questradeAPI"))) # append questradeAPI directory path

print(sys.path)

import smtplib
import math
import requests
import time
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from credentials import ESHINHW_ACCOUNT_TYPE, ESHINHW_QUESTRADE_API_CODE
from credentials import ALWL6782_ACCOUNT_TYPE, ALWL6782_QUESTRADE_API_CODE
from email.message import EmailMessage
from credentials import GMAIL_ADDRESS, GMAIL_PW

def sendEmail(subject, stock_bal, stock_port, quant_bal, quant_port):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = GMAIL_ADDRESS

    msg.add_alternative(
        f"""\

        <!DOCTYPE html>
        <html>
            <body>
                <p> Hello Investors,<br> Below is the daily summary of your portfolio and updated stock watchlist.<br> Have a good evening :) </p>
                <h1> Stock Portfolio Overview </h1>
                <h3> Balance Summary </h3>
                {stock_bal}
                <h3> Performance Summary </h3>
                {stock_port}
                <br>
                <h1> Quant Portfolio Overview </h1>
                <h3> Balance Summary </h3>
                {quant_bal}
                <h3> Performance Summary </h3>
                {quant_port}
                <br>
            </body>
        </html>
    """,
        subtype="html",
    )
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, GMAIL_PW)
        smtp.send_message(msg)

sendEmail('Questrade Portfolios Daily Report', stock_bal.to_html(), stock_portfolio.to_html(), quant_bal.to_html(), quant_portfolio.to_html())
