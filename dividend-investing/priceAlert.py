import os
import datetime as dt
import email_sender as email
import pandas_datareader.data as web

watchlist = [('MO', 45), # Altria Group
             ('SBUX', 100) # Starbucks
             ]


startDate = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
endDate = dt.date.today().strftime("%Y-%m-%d")
EMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

for stock in watchlist:
    symbol = stock[0]
    targetPrice = stock[1]
    close = web.DataReader(symbol, 'yahoo', startDate, endDate)['Adj Close'].iloc[-1].round(2)
    if close <= targetPrice:
        email.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD,
                        'Time to consider buying ' + symbol, 'Recent close price is $' + str(close))
        print("Alert email about " + symbol + " has been sent!")

