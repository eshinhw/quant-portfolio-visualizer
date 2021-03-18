import os
import datetime as dt
import email_sender as email
from qtrade import Questrade
import schedule
import time

watchlist = [('MO', 45), # Altria Group
             ('SBUX', 100) # Starbucks
             ]




qt = Questrade(token_yaml=r'C:\Users\eshin\Desktop\GitHub\quantitative-finance-and-investing\dividend-investing\access_token.yml')
qt.refresh_access_token(from_yaml=True)


startDate = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
endDate = dt.date.today().strftime("%Y-%m-%d")
EMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

for stock in watchlist:
    symbol = stock[0]
    targetPrice = stock[1]
    data = qt.get_historical_data(symbol, startDate, endDate, 'OneDay')
    close = data[1]['close']
    if close <= targetPrice:
        email.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD,
                        'Time to consider buying ' + symbol, 'Recent close price is $' + str(close))
        print("Alert email about " + symbol + " has been sent!")

