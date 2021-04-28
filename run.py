import time
# import schedule
import auto_email
import pandas as pd
import datetime as dt
import pandas_datareader.data as web

def calculate_prev_max_high(symbol: str, period: int):
    # start_date = dt.datetime.today() - dt.timedelta(days=period)
    # end_date = dt.datetime.today()
    prices = web.DataReader(symbol, 'yahoo')
    prices["High_" + str(period)] = prices["High"].shift(1).rolling(window=period).max()
    return prices["High_" + str(period)].iloc[-1]

def get_current_price(symbol: str) -> float:
    start_date = dt.datetime.today() - dt.timedelta(days=4)
    end_date = dt.datetime.today()
    prices = web.DataReader(symbol, 'yahoo', start_date, end_date)
    return prices['Adj Close'].iloc[-1]

def iterate_df():
    df = pd.read_csv('./export_df_rpi.csv')
    df.set_index('Symbol', inplace=True)


    for symbol in list(df.index):
        high = calculate_prev_max_high(symbol,252)
        curr_price = get_current_price(symbol)
        # print(f"high: {high}, current_price: {curr_price}")
        df.loc[symbol,'12M_High'] = high
        df.loc[symbol,'Current_Price'] = curr_price
        df.loc[symbol,'15%_Drop'] = high * 0.85
        df.loc[symbol,'30%_Drop'] = high * 0.70
        df.loc[symbol,'50%_Drop'] = high * 0.5
        drop_15 = df.loc[symbol,'15%_Drop']
        drop_30 = df.loc[symbol,'30%_Drop']
        drop_50 = df.loc[symbol,'50%_Drop']
        if curr_price < drop_15 and curr_price > drop_30:
            subject = f"15% DROP PRICE ALERT - {symbol}"
            contents = f"{symbol} has dropped more than 15% from 52W High. It's time to consider buying some shares of it."
            auto_email.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents)
        elif curr_price < drop_30 and curr_price > drop_50:
            subject = f"30% DROP PRICE ALERT - {symbol}"
            contents = f"{symbol} has dropped more than 30% from 52W High. Should I buy more?"
            auto_email.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents)
        elif curr_price < drop_50:
            subject = f"50% DROP PRICE ALERT - {symbol}"
            contents = f"{symbol} has dropped more than 50% from 52W High. Definitely panic market!"
            auto_email.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents)

    print(df)


##############################################################################
## Drawdowns From 52 Weeks High + Email Alert Setup
##############################################################################

if __name__ == '__main__':

    with open('./credentials/gmail.txt', 'r') as fp:
        secret = fp.readlines()
        EMAIL_ADDRESS = secret[0].rstrip('\n')
        EMAIL_PASSWORD = secret[1]
        fp.close()

    while True:
        iterate_df()
        time.sleep(1800)


