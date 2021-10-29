import time
from oandaTrader import OandaTrader
from demo_credentials import OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID

# Login
oanda = OandaTrader(OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID)

INSTRUMENTS = oanda.fx_instruments()

# 1H SETUP
INTERVAL = 'H1'
MA_LAGGING_PERIOD = -36
SMA = 120
LMA = 720
ATR_PERIOD = 480
RISK_PER_TRADE = 0.01
ATR_MULTIPLIER = 3

# DAILY SETUP
# INTERVAL = 'D'
# MA_LAGGING_PERIOD = -5
# SMA = 60
# LMA = 252
# ATR_PERIOD = 252
# RISK_PER_TRADE = 0.01
# ATR_MULTIPLIER = 2.5

count = 0

for symbol in INSTRUMENTS:
    count += 1
    # print(f"{symbol}\t : \t {count}/{len(INSTRUMENTS)}")
    try:
        ohlc = oanda.get_ohlc(symbol, LMA * 2, INTERVAL)
        ohlc[f'{SMA}MA'] = ohlc['Close'].rolling(SMA).mean()
        ohlc[f'{LMA}MA'] = ohlc['Close'].rolling(LMA).mean()

        trades_list = oanda.get_trade_list()
        orders_list = oanda.get_order_list()

        prev_sma = ohlc.iloc[MA_LAGGING_PERIOD][f'{SMA}MA']
        prev_lma = ohlc.iloc[MA_LAGGING_PERIOD][f'{LMA}MA']
        curr_sma = ohlc.iloc[-1][f'{SMA}MA']
        curr_lma = ohlc.iloc[-1][f'{LMA}MA']

        curr_low = oanda.get_current_low(symbol, 5, INTERVAL)
        curr_high = oanda.get_current_high(symbol, 5, INTERVAL)

        # print('stop_pips:', oanda.calculate_ATR(symbol, ATR_PERIOD, INTERVAL) * ATR_MULTIPLIER)

        # bullish cross over --> long
        if prev_sma < prev_lma and prev_sma > prev_lma:
            entry = oanda.get_current_ask_bid_price(symbol)[0]
            stop = entry - oanda.calculate_ATR(symbol, ATR_PERIOD, INTERVAL) * ATR_MULTIPLIER
            if (entry > curr_lma) and (curr_low > curr_lma):
                if (symbol not in trades_list) and (symbol not in orders_list):
                    oanda.create_limit_order(symbol, entry, stop, RISK_PER_TRADE)
                    print(f"Order Placed [{symbol}] @ ENTRY: {entry} SL: {stop}")

        # bearish cross over --> short
        if prev_sma > prev_lma and curr_sma < curr_lma:
            entry = oanda.get_current_ask_bid_price(symbol)[1]
            stop = entry - oanda.calculate_ATR(symbol, ATR_PERIOD, INTERVAL) * ATR_MULTIPLIER
            if (entry < curr_lma) and (curr_high < curr_lma):
                if (symbol not in trades_list) and (symbol not in orders_list):
                    oanda.create_limit_order(symbol, entry, stop, RISK_PER_TRADE)
                    print(f"Order Placed [{symbol}] @ ENTRY: {entry} SL: {stop}")

        time.sleep(1)

    except Exception as e:
        print(e)

print("Run Successfully --------- " + time.ctime())