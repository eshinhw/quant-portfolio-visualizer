import time
import schedule
import auto_email
import pandas as pd
import datetime as dt
import pandas_datareader.data as web

SENT = {}

def calculate_prev_max_high(symbol: str, period: int):
    start_date = dt.datetime(1970,1,1)
    end_date = dt.datetime.today()
    prices = web.DataReader(symbol, 'yahoo', start_date, end_date)
    #print(prices)
    prices["High_" + str(period)] = prices["High"].shift(1).rolling(window=period).max()
    return prices["High_" + str(period)].iloc[-1]

def get_current_price(symbol: str) -> float:
    start_date = dt.datetime.today() - dt.timedelta(days=4)
    end_date = dt.datetime.today()
    prices = web.DataReader(symbol, 'yahoo', start_date, end_date)
    return prices['Adj Close'].iloc[-1]

def iterate_df():
    df = pd.read_csv('./qualified_df.csv')
    df.set_index('Symbol', inplace=True)

    op1 = ('15%', 0.85)
    op2 = ('20%', 0.80)
    op3 = ('30%', 0.70)
    op4 = ('50%', 0.50)

    count = 0

    for symbol in list(df.index):
        count += 1
        print(f"{symbol}:\t{count}/{len(list(df.index))}")
        try:
            high = calculate_prev_max_high(symbol,252)
            curr_price = get_current_price(symbol)
        except:
            continue
        df.loc[symbol,'12M_High'] = high
        df.loc[symbol,'Current_Price'] = curr_price
        df.loc[symbol,f'{op1[0]}_Drop'] = high * op1[1]
        df.loc[symbol,f'{op2[0]}_Drop'] = high * op2[1]
        df.loc[symbol,f'{op3[0]}_Drop'] = high * op3[1]
        df.loc[symbol,f'{op4[0]}_Drop'] = high * op4[1]
        drop1 = df.loc[symbol,f'{op1[0]}_Drop']
        drop2 = df.loc[symbol,f'{op2[0]}_Drop']
        drop3 = df.loc[symbol,f'{op3[0]}_Drop']
        drop4 = df.loc[symbol,f'{op4[0]}_Drop']
        if curr_price < drop1 and curr_price > drop2:
            subject = f"{op1[0]} DROP PRICE ALERT - {symbol}"
            contents = f"{symbol} has dropped more than {op1[0]} from 52W High ({high}).\n\nCurrent Price: {curr_price}\n Target: {drop1}"
            auto_email.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents)
        elif curr_price < drop2 and curr_price > drop3:
            subject = f"{op2[0]} DROP PRICE ALERT - {symbol}"
            contents = f"{symbol} has dropped more than {op2[0]} from 52W High ({high}).\n\nCurrent Price: {curr_price}\n Target: {drop2}"
            auto_email.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents)
        elif curr_price < drop3 and curr_price > drop4:
            subject = f"{op3[0]} DROP PRICE ALERT - {symbol}"
            contents = f"{symbol} has dropped more than {op3[0]} from 52W High ({high}).\n\nCurrent Price: {curr_price}\n Target: {drop3}"
            auto_email.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents)
        elif curr_price < drop4:
            subject = f"{op4[0]} DROP PRICE ALERT - {symbol}"
            contents = f"{symbol} has dropped more than {op4[0]} from 52W High ({high}).\n\nCurrent Price: {curr_price}\n Target: {drop4}"
            auto_email.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents)

    # #print(df)
    # subject = "DAILY PRICE CHECK COMPLETED!"
    # # contents = """ALL THE STOCKS IN THE DATAFRAME HAVE BEEN CHECKED UP!\n\n
    # #             {}""".format(df.to_string())
    # contents = """<h3>Please find data attached and below.</h3>
    #                {}""".format(df.to_html())
    # auto_email.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents)

##############################################################################
## Drawdowns From 52 Weeks High + Email Alert Setup
##############################################################################

if __name__ == '__main__':

    with open('./credentials/gmail.txt', 'r') as fp:
        secret = fp.readlines()
        EMAIL_ADDRESS = secret[0].rstrip('\n')
        EMAIL_PASSWORD = secret[1]
        fp.close()

    schedule.every().day.at("17:30").do(iterate_df)
    # schedule.every().minute.do(iterate_df)
    # seconds = 0

    while True:
        schedule.run_pending()
        # seconds += 1
        # print(f"seconds running: {seconds}")
        time.sleep(1)







