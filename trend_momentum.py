import time
from oandaTrader import OandaTrader
from demo_credentials import OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID

# Login
oanda = OandaTrader(OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID)

INSTRUMENTS = oanda.fx_instruments()
MA_LAGGING_DAYS = -5
SMA = 60
LMA = 252
ATR_DAYS = 252
RISK_PER_TRADE = 0.01
ATR_MULTIPLIER = 2.5

# while True:
for symbol in INSTRUMENTS:
    try:
        ohlc = oanda.get_ohlc(symbol, 260, 'D')
        ohlc['60MA'] = ohlc['Close'].rolling(SMA).mean()
        ohlc['252MA'] = ohlc['Close'].rolling(LMA).mean()

        trades_list = oanda.get_trade_list()
        orders_list = oanda.get_order_list()

        prev_sma = ohlc.iloc[MA_LAGGING_DAYS]['60MA']
        prev_lma = ohlc.iloc[MA_LAGGING_DAYS]['252MA']
        curr_sma = ohlc.iloc[-1]['60MA']
        curr_lma = ohlc.iloc[-1]['252MA']

        # bullish cross over --> long
        if prev_sma < prev_lma and prev_sma > prev_lma:
            if (symbol not in trades_list) and (symbol not in orders_list):
                # long entry
                entry = oanda.get_current_ask_bid_price(symbol)[0]
                stop = entry - oanda.calculate_ATR(symbol, ATR_DAYS, 'D') * ATR_MULTIPLIER
                oanda.create_limit_order(symbol, entry, stop, RISK_PER_TRADE)

        # bearish cross over --> short
        if prev_sma > prev_lma and curr_sma < curr_lma:
            # short entry
            if (symbol not in trades_list) and (symbol not in orders_list):
                entry = oanda.get_current_ask_bid_price(symbol)[1]
                stop = entry - oanda.calculate_ATR(symbol, ATR_DAYS, 'D') * ATR_MULTIPLIER
                oanda.create_limit_order(symbol, entry, stop, RISK_PER_TRADE)


    except Exception as e:
        print(e)
        time.sleep(1)