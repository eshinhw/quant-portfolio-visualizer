import time
import datetime
from demo_credentials import OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID
from oandaTrader import OandaTrader

K = 0.5
FEE = 0.0050
INSTRUMENTS = ['EUR_USD']

# Login
oanda = OandaTrader(OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID)

trade_log = {}

# while True:
for symbol in INSTRUMENTS:
    try:
        ohlc = oanda.get_ohlc(symbol, 260, 'D')
        ohlc['60MA'] = ohlc['Close'].rolling(60).mean()
        ohlc['252MA'] = ohlc['Close'].rolling(252).mean()
        print(ohlc)

        # entry rule
        prev_sma = ohlc.iloc[-3]['60MA']
        prev_lma = ohlc.iloc[-3]['252MA']
        curr_sma = ohlc.iloc[-1]['60MA']
        curr_lma = ohlc.iloc[-1]['252MA']

        entry = oanda.get_current_ask_bid_price(symbol)[0]
        stop = entry - oanda.calculate_ATR(symbol, 60, 'D') * 2

        oanda.create_limit_order(symbol, entry, stop)


        # # bullish cross over --> long
        # if prev_sma < prev_lma and prev_sma > prev_lma:
        #     # long entry
        #     entry = oanda.get_current_ask_bid_price(symbol)[0]
        #     stop = entry - oanda.calculate_ATR(symbol, 60, 'D') * 2
        #     distance = abs(entry - stop)


        # if prev_sma > prev_lma and curr_sma < curr_lma:
        #     # short entry
        #     pass

    except Exception as e:
        print(e)
        time.sleep(1)