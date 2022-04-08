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
from questradeAPI import Questrade
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

sendEmail('Questrade Portfolios Daily Report', stock_bal.to_html(), stock_portfolio.to_html(), quant_bal.to_html(), quant_portfolio.to_html())
print("Sent Successfully ------ " + time.ctime())

class FixedAllocation():

    def __init__(self,name,assets,weights) -> None:
        self.name = name
        self.assets = assets
        self.weights = weights
        self.port_cum_returns = self.cumulative_returns()

    def __str__(self) -> str:
        return self.name

    def daily_return(self):
        data = yf.download(self.assets, start = start, end = end)
        data = data.loc[:,'Adj Close']
        #data = data.loc[:,('Adj Close', slice(None))]
        data.columns = self.assets
        rets = data.pct_change().dropna()
        return rets

    def monthly_return(self):
        monthly_prices = pd.DataFrame()
        for asset in self.assets:
            monthly_prices[asset] = FMP_PRICES.get_monthly_prices(asset)[asset]
        monthly_returns = monthly_prices.pct_change()
        monthly_returns.dropna(inplace=True)
        
        return monthly_returns

    def cumulative_returns(self):
        prices = pd.DataFrame() 

        for symbol in self.assets:
            prices[symbol] = FMP_PRICES.get_monthly_prices(symbol)[symbol]

        prices.dropna(inplace=True)
        monthly_returns = prices.pct_change()
        monthly_returns = monthly_returns.shift(-1)
        monthly_returns['port'] = monthly_returns.dot(self.weights)
        cum_returns = np.exp(np.log1p(monthly_returns['port']).cumsum())[:-1]
        return cum_returns

    def cagr(self):
        first_value = self.port_cum_returns[0]
        last_value = self.port_cum_returns[-1]  
        years = len(self.port_cum_returns.index)/12    
        cagr = (last_value/first_value)**(1/years) - 1
        return cagr
    
    def mdd(self):
        previous_peaks = self.port_cum_returns.cummax()
        drawdown = (self.port_cum_returns - previous_peaks) / previous_peaks
        port_mdd = drawdown.min()
        return port_mdd

    def report(self):
        rets = self.daily_return()

        port = rp.Portfolio(returns=rets)
        w = pd.DataFrame(self.weights, index = self.assets)
        ax = rp.jupyter_report(rets, w, rm='MV', rf=0, alpha=0.05, height=6, width=14,
                       others=0.05, nrow=25)
        
        return ax