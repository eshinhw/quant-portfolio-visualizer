import json
import time
import datetime
from oandapyV20 import API
import oandapyV20.endpoints.trades as trades
from demo_credentials import OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID
from oandaTrader import OandaTrader

K = 0.5
FEE = 0.0050
INSTRUMENTS = ['EUR_USD']

# Login
oanda = OandaTrader(OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID)

def get_target_price(symbol, K):
    df = oanda.get_ohlc(symbol, 2, 'D')
    target_price = df.iloc[0]['Close'] + (df.iloc[0]['High'] - df.iloc[0]['Low']) * K
    return target_price

def get_start_time(symbol):
    """returns start time"""
    df = oanda.get_ohlc(symbol, 2, 'D')
    start_time = df.index[0]
    return start_time

def get_current_ask_price(symbol):
    """returns ask price"""
    return oanda.get_current_ask_bid_price(symbol)[0]

def get_current_bid_price(symbol):
    """returns ask price"""
    return oanda.get_current_ask_bid_price(symbol)[1]

# 자동매매 시작
while True:
    for symbol in INSTRUMENTS:
        try:

            now = datetime.datetime.now()
            start_time = get_start_time(symbol)
            end_time = start_time + datetime.timedelta(days=1)
            print(f"running ...{symbol}...{str(now)}")
            # open a trade
            if start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price(symbol, K)
                ma = oanda.calculate_MA(symbol, 20, 'D')
                current_ask_price = get_current_ask_price(symbol)
                current_bid_price = get_current_bid_price(symbol)
                if ma < current_bid_price and target_price < current_bid_price:
                    oanda.create_buy_market_order()
                if ma > current_ask_price and target_price > current_ask_price:
                    oanda.create_sell_market_order()

            # close a trade
            else:
                oanda.close_open_trade(symbol)
            time.sleep(1)

        except Exception as e:
            print(e)
            time.sleep(1)


