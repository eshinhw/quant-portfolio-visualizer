import os
import time
from credentials import API_OANDA, VB_ACCT, DEMO_ACCT
from oanda import Oanda

# Login
if os.name == 'nt':
    oanda = Oanda(API_OANDA, VB_ACCT)
if os.name == 'posix':
    oanda = Oanda(API_OANDA, DEMO_ACCT)

RISK_PER_TRADE = 0.0002

ORDERS_LIST = oanda.get_order_list()
TRADES_LIST = oanda.get_trade_list()

SYMBOLS_ORDERS = oanda.symbols_in_orders()
SYMBOLS_TRADES = oanda.symbols_in_trades()

K = 0.5

def open_trades(symbol):
    df = oanda.get_ohlc(symbol, 6, 'D')
    prev_range = (df['High'] - df['Low'])[-2]
    prev_high = df.iloc[-2]['High']
    prev_low = df.iloc[-2]['Low']

    stop_long_entry = prev_high + (prev_range * K)
    stop_sl = prev_low
    oanda.create_stop_order(symbol, stop_long_entry, stop_sl, RISK_PER_TRADE)

    stop_short_entry = prev_low - (prev_range * K)
    stop_sl = prev_high
    oanda.create_stop_order(symbol, stop_short_entry, stop_sl, RISK_PER_TRADE)

if __name__ == '__main__':
    symbol = 'EUR_USD'
    open_trades(symbol)
    print("Open Trades::: " + time.ctime())