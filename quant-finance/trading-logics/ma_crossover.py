import os
import time
import datetime as dt
from pprint import pprint
from oanda import Oanda
from credentials import API_OANDA, CROSSOVER_ACCT

# Login

if os.name == 'nt':
    oanda = Oanda(API_OANDA, CROSSOVER_ACCT)
if os.name == 'posix':
    oanda = Oanda(API_OANDA, CROSSOVER_ACCT)

OPEN_ORDERS = oanda.get_order_list()
OPEN_TRADES = oanda.get_trade_list()

SYMBOLS_ORDERS = oanda.symbols_in_orders()
SYMBOLS_TRADES = oanda.symbols_in_trades()

# DAILY SETUP
SMA = 120
LMA = 480
INTERVAL = 'D'
MA_LAGGING_PERIOD = -3
SL_PERCENT = 0.025
RISK_PER_TRADE = 0.02

# open trades

def bullish_crossover_test(symbol):
    ohlc = oanda.get_ohlc(symbol, LMA * 2, INTERVAL)
    sma = f'{SMA}MA'
    lma = f'{LMA}MA'
    ohlc[sma] = ohlc['Close'].rolling(SMA).mean()
    ohlc[lma] = ohlc['Close'].rolling(LMA).mean()

    prev_sma = ohlc[sma].iloc[MA_LAGGING_PERIOD]
    prev_lma = ohlc[lma].iloc[MA_LAGGING_PERIOD]

    curr_sma = ohlc[sma].iloc[-1]
    curr_lma = ohlc[lma].iloc[-1]

    curr_close = ohlc['Close'].iloc[-1]
    curr_low = ohlc['Low'].iloc[-1]

    return prev_sma < prev_lma and curr_sma > curr_lma and curr_close > curr_sma and curr_low > curr_sma

def bearish_crossover_test(symbol):
    ohlc = oanda.get_ohlc(symbol, LMA * 2, INTERVAL)
    sma = f'{SMA}MA'
    lma = f'{LMA}MA'
    ohlc[sma] = ohlc['Close'].rolling(SMA).mean()
    ohlc[lma] = ohlc['Close'].rolling(LMA).mean()

    prev_sma = ohlc[sma].iloc[MA_LAGGING_PERIOD]
    prev_lma = ohlc[lma].iloc[MA_LAGGING_PERIOD]

    curr_sma = ohlc[sma].iloc[-1]
    curr_lma = ohlc[lma].iloc[-1]

    curr_close = ohlc['Close'].iloc[-1]
    curr_high = ohlc['High'].iloc[-1]

    return prev_sma > prev_lma and curr_sma < curr_lma and curr_close < curr_sma and curr_high < curr_sma

def open_trades(symbol):
    try:
        # bullish cross over --> long
        if bullish_crossover_test(symbol):

            # Determine entry and stop price
            entry = oanda.get_current_ask_bid_price(symbol)[0]
            stop = entry - (entry * SL_PERCENT)

            if (symbol not in SYMBOLS_TRADES) and (symbol not in SYMBOLS_ORDERS):
                oanda.create_limit_order(symbol, entry, stop, RISK_PER_TRADE)
                print(f"Long Order Placed [{symbol}] @ ENTRY: {entry} SL: {stop}")
            else:
                # there exists a trade in opposite direction which must be closed first.
                oanda.close_open_trade(symbol)
                oanda.create_limit_order(symbol, entry, stop, RISK_PER_TRADE)

        # bearish cross over --> short
        if bearish_crossover_test(symbol):

            # Determine entry and stop price
            entry = oanda.get_current_ask_bid_price(symbol)[1]
            stop = entry + (entry * SL_PERCENT)

            if (symbol not in SYMBOLS_TRADES) and (symbol not in SYMBOLS_ORDERS):
                oanda.create_limit_order(symbol, entry, stop, RISK_PER_TRADE)
                print(f"Short Order Placed [{symbol}] @ ENTRY: {entry} SL: {stop}")
            else:
                # there exists a trade in opposite direction which must be closed first.
                oanda.close_open_trade(symbol)
                oanda.create_limit_order(symbol, entry, stop, RISK_PER_TRADE)

    except Exception as e:
        print(e)


if __name__ == "__main__":

    # open_trades('EURUSD')
    # print("Run Successfully --> " + time.ctime())

    a = ('1')
    dict_a = {}
    dict_a['b'] = a

