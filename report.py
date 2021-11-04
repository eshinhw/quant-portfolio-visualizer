import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "questradeAPI"))) # append questradeAPI directory path

import smtplib
import math
import requests
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from questradeAPI.credentials import ESHINHW_ACCOUNT_TYPE, ESHINHW_QUESTRADE_API_CODE
from questradeAPI.credentials import ALWL6782_ACCOUNT_TYPE, ALWL6782_QUESTRADE_API_CODE
from questradeAPI import Questrade
from email.message import EmailMessage
from questradeAPI.credentials import GMAIL_ADDRESS, GMAIL_PW

def sendEmail(subject, curr_pos, filters, watchlist):
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
                <h1> Portfolio Overview </h1>
                <h3> Balance Summary </h3>
                {curr_pos}
                <h3> Performance Summary </h3>
                {filters}
                <br>
                {watchlist}
            </body>
        </html>
    """,
        subtype="html",
    )
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, GMAIL_PW)
        smtp.send_message(msg)

USER_ID = 'eshinhw'
ACCOUNT_TYPE = ESHINHW_ACCOUNT_TYPE
QUESTRADE_CODE = ESHINHW_QUESTRADE_API_CODE

# print(os.getcwd())

try:
    qbot = Questrade(USER_ID)
    acctNums = qbot.accounts
except:
    # print(os.getcwd())
#     os.remove(os.getcwd())
    qbot = Questrade(USER_ID, refresh_token=QUESTRADE_CODE)

acctData = {}
acctNums = qbot.accounts
for aNum in acctNums:
    if aNum in ACCOUNT_TYPE:
        aName = ACCOUNT_TYPE[aNum]
        if aName == 'Stock Portfolio':
            stock_bal = qbot.account_balances(aNum)
            stock_portfolio = qbot.account_positions(aNum)
            stock_return = qbot.portfolio_return(aNum)
#             stock_dividends = qbot.get_dividend_income(aNum)
        if aName == 'Quant Portfolio':
            quant_bal = qbot.account_balances(aNum)
            quant_portfolio = qbot.account_positions(aNum)
            quant_return = qbot.portfolio_return(aNum)
#             quant_dividends = qbot.get_dividend_income(aNum)
    else:
        print("Please define portfolio first in credentials.py")

sendEmail('Stock Portfolio', stock_bal.to_html(), stock_portfolio.to_html(), stock_bal.to_html())
sendEmail('Quant Portfolio', quant_bal.to_html(), quant_portfolio.to_html(), quant_bal.to_html())