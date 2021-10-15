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
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = oanda.get_ohlc(symbol, 2, 'D')
    #df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['Close'] + (df.iloc[0]['High'] - df.iloc[0]['Low']) * K
    return target_price

def get_start_time(symbol):
    """시작 시간 조회"""
    df = oanda.get_ohlc(symbol, 2, 'D')
    start_time = df.index[0]
    return start_time

def get_current_price(symbol):
    """현재가 조회"""
    return oanda.get_current_ask_bid_price(symbol)[0]



# 자동매매 시작
while True:
    for symbol in INSTRUMENTS:
        try:
            now = datetime.datetime.now()
            start_time = get_start_time(symbol)
            end_time = start_time + datetime.timedelta(days=1)

            # open a trade
            if start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price(symbol, K)
                ma = oanda.calculate_MA(symbol, 15, 'D')
                current_price = get_current_price(symbol)
                if target_price < current_price and ma < current_price:
                    oanda.create_buy_market_order()

            # close a trade
            else:
                oanda.close_open_trade(symbol)
            time.sleep(1)

        except Exception as e:
            print(e)
            time.sleep(1)


