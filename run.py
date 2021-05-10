import time
import schedule
import auto_email
import pandas as pd
import datetime as dt
import pandas_datareader.data as web
from stock_selection import construct_stock_df_to_csv


def calculate_prev_max_high(symbol: str, period: int):
    start_date = dt.datetime(1970,1,1)
    end_date = dt.datetime.today()
    prices = web.DataReader(symbol, 'yahoo', start_date, end_date)
    prices["High_" + str(period)] = prices["High"].shift(1).rolling(window=period).max()
    return prices["High_" + str(period)].iloc[-1]

def get_current_price(symbol: str) -> float:
    start_date = dt.datetime.today() - dt.timedelta(days=4)
    end_date = dt.datetime.today()
    prices = web.DataReader(symbol, 'yahoo', start_date, end_date)
    return prices['Adj Close'].iloc[-1]

def send_contents(alert_list):
    subject = f"STOCK PRICE ALERT"
    contents = ""
    for data in alert_list:
        symbol = data[0]
        percentage = data[1]
        prev_high = data[2]
        current = data[3]
        target = data[4]
        contents += f"{symbol} has dropped more than {percentage} from 52W High ({prev_high}).\n\nCurrent Price: {current}\nTarget: {target}\n"

    auto_email.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents)

def iterate_df():
    alert_list = []
    df = pd.read_csv('./stock_selection.csv')
    df.set_index('Symbol', inplace=True)

    op1 = ('10%', 0.90)
    op2 = ('15%', 0.85)
    op3 = ('20%', 0.80)
    op4 = ('30%', 0.70)
    op5 = ('50%', 0.50)

    count = 0
    print("::::: INSERT PULLBACK PRICE DATA :::::")
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
        df.loc[symbol,f'{op5[0]}_Drop'] = high * op5[1]
        drop1 = df.loc[symbol,f'{op1[0]}_Drop']
        drop2 = df.loc[symbol,f'{op2[0]}_Drop']
        drop3 = df.loc[symbol,f'{op3[0]}_Drop']
        drop4 = df.loc[symbol,f'{op4[0]}_Drop']
        drop5 = df.loc[symbol,f'{op5[0]}_Drop']
        if curr_price < drop1 and curr_price > drop2:
            alert_list.append((symbol, op1[0], high, curr_price, drop1))
        elif curr_price < drop2 and curr_price > drop3:
            alert_list.append((symbol, op2[0], high, curr_price, drop2))
        elif curr_price < drop3 and curr_price > drop4:
            alert_list.append((symbol, op3[0], high, curr_price, drop3))
        elif curr_price < drop4 and currPrice > drop5:
            alert_list.append((symbol, op4[0], high, curr_price, drop4))
        elif curr_price < drop5:
            alert_list.append((symbol, op5[0], high, curr_price, drop5))
    print(df)
    print('end of iteration')

    if len(alert_list) > 0:
        print("alert_list is not empty!")
        send_contents(alert_list)




##############################################################################
## Drawdowns From 52 Weeks High + Email Alert Setup
##############################################################################

if __name__ == '__main__':

    with open('./credentials/gmail.txt', 'r') as fp:
        secret = fp.readlines()
        EMAIL_ADDRESS = secret[0].rstrip('\n')
        EMAIL_PASSWORD = secret[1]
        fp.close()

    afternoon = '13:00'
    afternoon_check = '13:15'
    evening = '17:00'
    evening_check = '17:15'

    schedule.every().monday.at(afternoon).do(construct_stock_df_to_csv)
    schedule.every().tuesday.at(afternoon).do(construct_stock_df_to_csv)
    schedule.every().wednesday.at(afternoon).do(construct_stock_df_to_csv)
    schedule.every().thursday.at(afternoon).do(construct_stock_df_to_csv)
    schedule.every().friday.at(afternoon).do(construct_stock_df_to_csv)


    schedule.every().monday.at(afternoon_check).do(iterate_df)
    schedule.every().tuesday.at(afternoon_check).do(iterate_df)
    schedule.every().wednesday.at(afternoon_check).do(iterate_df)
    schedule.every().thursday.at(afternoon_check).do(iterate_df)
    schedule.every().friday.at(afternoon_check).do(iterate_df)

    schedule.every().monday.at(evening).do(construct_stock_df_to_csv)
    schedule.every().tuesday.at(evening).do(construct_stock_df_to_csv)
    schedule.every().wednesday.at(evening).do(construct_stock_df_to_csv)
    schedule.every().thursday.at(evening).do(construct_stock_df_to_csv)
    schedule.every().friday.at(evening).do(construct_stock_df_to_csv)


    schedule.every().monday.at(evening_check).do(iterate_df)
    schedule.every().tuesday.at(evening_check).do(iterate_df)
    schedule.every().wednesday.at(evening_check).do(iterate_df)
    schedule.every().thursday.at(evening_check).do(iterate_df)
    schedule.every().friday.at(evening_check).do(iterate_df)

    schedule.every().sunday.at("20:20").do(construct_stock_df_to_csv)
    schedule.every().sunday.at("20:25").do(iterate_df)

    while True:
        schedule.run_pending()
        #time.sleep(1)







