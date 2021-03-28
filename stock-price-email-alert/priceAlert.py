import os
import smtplib
import datetime as dt
import pandas_datareader.data as web
from email.message import EmailMessage

watchlist = [('MO', 45), # Altria Group
             ('SBUX', 100), # Starbucks
             ('ABBV', 100) #
             ]

def sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents):
    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    msg.set_content(contents)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def main():
    startDate = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    endDate = dt.date.today().strftime("%Y-%m-%d")
    EMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
    EMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

    for stock in watchlist:
        symbol = stock[0]
        targetPrice = stock[1]
        close = web.DataReader(symbol, 'yahoo', startDate, endDate)['Adj Close'].iloc[-1].round(2)
        #print(close)
        if close <= targetPrice:
            sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD,
                            'Time to consider buying ' + symbol, 'Recent close price is $' + str(close))
            print("Alert email about " + symbol + " has been sent!")

    print("End of Price Check")

if __name__ == '__main__':
    main()
