import time
import os
import datetime as dt
from pprint import pprint
from oandaTrader import OandaTrader
from demo_credentials import OANDA_API_KEY, TREND_FOLLOWING_ACCOUNT_ID, TEST_ACCOUNT_ID

# Login
if os.name == 'nt':
    oanda = OandaTrader(OANDA_API_KEY, TEST_ACCOUNT_ID)
if os.name == 'posix':
    oanda = OandaTrader(OANDA_API_KEY, TREND_FOLLOWING_ACCOUNT_ID)

INSTRUMENTS = oanda.fx_instruments()

ORDERS_LIST = oanda.get_order_list()
TRADES_LIST = oanda.get_trade_list()

SYMBOLS_ORDERS = oanda.symbols_in_orders()
SYMBOLS_TRADES = oanda.symbols_in_trades()

DECIMAL_TABLE = oanda.create_decimal_table()

# 1H SETUP
INTERVAL = 'H1'
SMA = 120
LMA = 720
ATR_PERIOD = 480
RISK_PER_TRADE = 0.005
SL_MULTIPLIER = 3
PREV_KEY_LEVEL_BUFFER = 3
WAIT_PERIOD = 12
ENTRY_STOP_BUFFER = 3

# DAILY SETUP
# INTERVAL = 'D'
# MA_LAGGING_PERIOD = -5
# SMA = 60
# LMA = 252
# ATR_PERIOD = 252
# RISK_PER_TRADE = 0.01
# ATR_MULTIPLIER = 2.5

# open trades

def bullish_crossover_test(symbol):
    ohlc = oanda.get_ohlc(symbol, LMA * 2, INTERVAL)
    ohlc[f'{SMA}MA'] = ohlc['Close'].rolling(SMA).mean()
    ohlc[f'{LMA}MA'] = ohlc['Close'].rolling(LMA).mean()

    curr_date = ohlc.index[-1]
    try:
        bullish_crossover_date = ohlc[ohlc[f'{SMA}MA'] < ohlc[f'{LMA}MA']].index[-1] + dt.timedelta(hours=1)
        entry_date = bullish_crossover_date + dt.timedelta(hours=WAIT_PERIOD)
    except:
        return False
    # print(type(curr_date))
    # print(curr_date)
    # print(bullish_crossover_date)
    # print(entry_date)
    # print(curr_date == entry_date)

    return curr_date == entry_date

def bearish_crossover_test(symbol):
    # print(symbol)
    ohlc = oanda.get_ohlc(symbol, LMA * 2, INTERVAL)
    ohlc[f'{SMA}MA'] = ohlc['Close'].rolling(SMA).mean()
    ohlc[f'{LMA}MA'] = ohlc['Close'].rolling(LMA).mean()

    curr_date = ohlc.index[-1]

    try:
        bearish_crossover_date = ohlc[ohlc[f'{SMA}MA'] > ohlc[f'{LMA}MA']].index[-1] + dt.timedelta(hours=1)
        entry_date = bearish_crossover_date + dt.timedelta(hours=WAIT_PERIOD)
    except:
        # print('return False')
        return False

    # print(type(curr_date))
    # print(curr_date)
    # print(bearish_crossover_date)
    # print(entry_date)
    # print(curr_date == entry_date)

    return curr_date == entry_date

def open_trades():
    count = 0
    for symbol in INSTRUMENTS:
        count += 1
        print(f"{symbol}\t : \t {count}/{len(INSTRUMENTS)}")

        decimal = DECIMAL_TABLE[symbol]['decimal']
        multiple = DECIMAL_TABLE[symbol]['multiple']

        try:
            # bullish cross over --> long
            if bullish_crossover_test(symbol):
                curr_low = oanda.get_current_low(symbol, WAIT_PERIOD, INTERVAL)
                curr_high = oanda.get_current_high(symbol, WAIT_PERIOD, INTERVAL)

                entry = round(curr_high + (ENTRY_STOP_BUFFER / multiple), decimal)

                stop_with_atr = entry - oanda.calculate_ATR(symbol, ATR_PERIOD, INTERVAL) * SL_MULTIPLIER
                stop_with_low = curr_low - (ENTRY_STOP_BUFFER / multiple)

                stop = round(min(stop_with_atr, stop_with_low), decimal)

                if (symbol not in SYMBOLS_TRADES) and (symbol not in SYMBOLS_ORDERS):
                    oanda.create_stop_order(symbol, entry, stop, RISK_PER_TRADE)
                    print(f"Order Placed [{symbol}] @ ENTRY: {entry} SL: {stop}")

            # bearish cross over --> short
            if bearish_crossover_test(symbol):
                curr_low = oanda.get_current_low(symbol, WAIT_PERIOD, INTERVAL)
                curr_high = oanda.get_current_high(symbol, WAIT_PERIOD, INTERVAL)

                entry = round(curr_low - (ENTRY_STOP_BUFFER / multiple), decimal)
                stop_with_atr = entry + oanda.calculate_ATR(symbol, ATR_PERIOD, INTERVAL) * SL_MULTIPLIER
                stop_with_high = curr_high + (ENTRY_STOP_BUFFER / multiple)
                stop = round(max(stop_with_atr, stop_with_high), decimal)

                if (symbol not in SYMBOLS_TRADES) and (symbol not in SYMBOLS_ORDERS):
                    oanda.create_stop_order(symbol, entry, stop, RISK_PER_TRADE)
                    print(f"Order Placed [{symbol}] @ ENTRY: {entry} SL: {stop}")

            time.sleep(1)

        except Exception as e:
            print(e)

def manage_stop_for_long(instrument, entry, sl_pips, rr_factor, support):
    if rr_factor >= 2 and rr_factor < 3:
        # if risk reward factor is 2.x, move stoploss to break even
        oanda.update_stop_loss(instrument, entry)
    else:
        new_sl = round(entry + (rr_factor - 2) * sl_pips, DECIMAL_TABLE[instrument]['decimal'])
        # if rr_factor is 3.x, change stop loss to 1.x (achieved 1:1 ratio)
        # if rr_factor is 4.x, change stop loss to 2.x (achieved 2:1 ratio)
        oanda.update_stop_loss(instrument, max(new_sl, support))

def manage_stop_for_short(instrument, entry, sl_pips, rr_factor, resistance):
    if rr_factor >= 2 and rr_factor < 3:
        # if risk reward factor is 2.x, move stoploss to break even
        oanda.update_stop_loss(instrument, entry)
    else:
        new_sl = round(entry - (rr_factor - 2) * sl_pips, DECIMAL_TABLE[instrument]['decimal'])
        # if rr_factor is 3.x, change stop loss to 1.x (achieved 1:1 ratio)
        # if rr_factor is 4.x, change stop loss to 2.x (achieved 2:1 ratio)
        oanda.update_stop_loss(instrument, min(new_sl, resistance))

def manage_trades():
    # systematically adjust stop loss
    for trade in TRADES_LIST:
        # print(trade)
        instrument = trade['instrument']
        entry = float(trade['price'])
        sl = float(trade['stopLossOrder']['price'])
        open_time = dt.datetime.strptime(trade['openTime'][:trade['openTime'].index('.')].replace('T', ' '),
                                         "%Y-%m-%d %H:%M:%S")
        curr_time = dt.datetime.now()
        diff = curr_time - open_time
        hours_diff = round(diff.seconds / 3600, 0)
        days_diff = round(diff.days, 0)
        sl_pips = abs(entry - sl)

        # long trade
        if sl < entry:
            curr_price = oanda.get_current_ask_bid_price(instrument)[1]
            profit_pips = abs(curr_price - entry)
            recent_low = oanda.calculate_prev_min_low(instrument, days_diff+PREV_KEY_LEVEL_BUFFER, 'D')
            atr = oanda.calculate_ATR(instrument, int(hours_diff), 'H1')
            support = round(recent_low - atr, DECIMAL_TABLE[instrument]['decimal'])
            rr_factor = profit_pips / sl_pips
            manage_stop_for_long(instrument, entry, sl_pips, rr_factor, support)

        # short trade
        else:
            curr_price = oanda.get_current_ask_bid_price(instrument)[0]
            profit_pips = abs(curr_price - entry)
            recent_high = oanda.calculate_prev_max_high(instrument, days_diff+PREV_KEY_LEVEL_BUFFER, 'D')
            atr = oanda.calculate_ATR(instrument, int(hours_diff), 'H1')
            resistance = round(recent_high + atr, DECIMAL_TABLE[instrument]['decimal'])
            rr_factor = profit_pips / sl_pips
            manage_stop_for_short(instrument, entry, sl_pips, rr_factor, resistance)


if __name__ == "__main__":

    open_trades()
    manage_trades()

    print("Run Successfully --------- " + time.ctime() + "---------------------------------")