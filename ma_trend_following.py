import os
import time
import datetime as dt
from pprint import pprint
from oandaTrader import OandaTrader
from credentials import OANDA_API_KEY, TREND_FOLLOWING_ACCOUNT_ID, TEST_ACCOUNT_ID

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

    return prev_sma < prev_lma and curr_sma > curr_lma

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

    return prev_sma > prev_lma and curr_sma < curr_lma

def open_trades():
    count = 0
    for symbol in INSTRUMENTS:
        count += 1
        #print(f"{symbol}\t : \t {count}/{len(INSTRUMENTS)}")

        # decimal = DECIMAL_TABLE[symbol]['decimal']
        # multiple = DECIMAL_TABLE[symbol]['multiple']

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

            time.sleep(1)

        except Exception as e:
            print(e)


if __name__ == "__main__":

    open_trades()
    print("Run Successfully --> " + time.ctime())

# def manage_stop_for_long(instrument, entry, sl_pips, rr_factor, support):

#     if rr_factor >= 1 and rr_factor < 2:
#         oanda.update_stop_loss(instrument, entry - sl_pips / 2)

#     if rr_factor >= 2 and rr_factor < 3:
#         # if risk reward factor is 2.x, move stoploss to break even
#         oanda.update_stop_loss(instrument, entry)
#     else:
#         new_sl = round(entry + (rr_factor - 2) * sl_pips, DECIMAL_TABLE[instrument]['decimal'])
#         # if rr_factor is 3.x, change stop loss to 1.x (achieved 1:1 ratio)
#         # if rr_factor is 4.x, change stop loss to 2.x (achieved 2:1 ratio)
#         oanda.update_stop_loss(instrument, max(new_sl, support))

# def manage_stop_for_short(instrument, entry, sl_pips, rr_factor, resistance):
#     if rr_factor >= 1 and rr_factor < 2:
#         oanda.update_stop_loss(instrument, entry + sl_pips / 2)

#     if rr_factor >= 2 and rr_factor < 3:
#         # if risk reward factor is 2.x, move stoploss to break even
#         oanda.update_stop_loss(instrument, entry)
#     else:
#         new_sl = round(entry - (rr_factor - 2) * sl_pips, DECIMAL_TABLE[instrument]['decimal'])
#         # if rr_factor is 3.x, change stop loss to 1.x (achieved 1:1 ratio)
#         # if rr_factor is 4.x, change stop loss to 2.x (achieved 2:1 ratio)
#         oanda.update_stop_loss(instrument, min(new_sl, resistance))

# def manage_trades():
#     # systematically adjust stop loss
#     for trade in TRADES_LIST:
#         # print(trade)
#         instrument = trade['instrument']
#         entry = float(trade['price'])
#         sl = float(trade['stopLossOrder']['price'])
#         open_time = dt.datetime.strptime(trade['openTime'][:trade['openTime'].index('.')].replace('T', ' '),
#                                          "%Y-%m-%d %H:%M:%S")
#         curr_time = dt.datetime.now()
#         diff = curr_time - open_time
#         hours_diff = round(diff.seconds / 3600, 0)
#         days_diff = round(diff.days, 0)
#         sl_pips = abs(entry - sl)

#         # long trade
#         if sl < entry:
#             curr_price = oanda.get_current_ask_bid_price(instrument)[1]
#             profit_pips = abs(curr_price - entry)
#             recent_low = oanda.calculate_prev_min_low(instrument, days_diff+PREV_KEY_LEVEL_BUFFER, 'D')
#             atr = oanda.calculate_ATR(instrument, int(hours_diff), 'H1')
#             support = round(recent_low - atr, DECIMAL_TABLE[instrument]['decimal'])
#             rr_factor = profit_pips / sl_pips
#             manage_stop_for_long(instrument, entry, sl_pips, rr_factor, support)

#         # short trade
#         else:
#             curr_price = oanda.get_current_ask_bid_price(instrument)[0]
#             profit_pips = abs(curr_price - entry)
#             recent_high = oanda.calculate_prev_max_high(instrument, days_diff+PREV_KEY_LEVEL_BUFFER, 'D')
#             atr = oanda.calculate_ATR(instrument, int(hours_diff), 'H1')
#             resistance = round(recent_high + atr, DECIMAL_TABLE[instrument]['decimal'])
#             rr_factor = profit_pips / sl_pips
#             manage_stop_for_short(instrument, entry, sl_pips, rr_factor, resistance)

