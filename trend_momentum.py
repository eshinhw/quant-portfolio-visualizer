import time
from pprint import pprint
from oandaTrader import OandaTrader
from demo_credentials import OANDA_API_KEY, TREND_FOLLOWING_ACCOUNT_ID

# Login
oanda = OandaTrader(OANDA_API_KEY, TREND_FOLLOWING_ACCOUNT_ID)

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



trades_list = oanda.get_trade_list()
orders_list = oanda.get_order_list()

# open trades

def open_trades():
    count = 0
    for symbol in INSTRUMENTS:
        count += 1
        # print(f"{symbol}\t : \t {count}/{len(INSTRUMENTS)}")
        try:
            ohlc = oanda.get_ohlc(symbol, LMA * 2, INTERVAL)
            ohlc[f'{SMA}MA'] = ohlc['Close'].rolling(SMA).mean()
            ohlc[f'{LMA}MA'] = ohlc['Close'].rolling(LMA).mean()

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

def manage_trades():
    # systematically adjust stop loss
    for trade in trades_list:
        instrument = trade['instrument']
        entry = float(trade['price'])
        sl = float(trade['stopLossOrder']['price'])
        tp = float(trade['takeProfitOrder']['price'])
        sl_pips = abs(entry - sl)
        # long trade
        if sl < entry:
            curr_price = oanda.get_current_ask_bid_price(instrument)[1]
            profit_pips = abs(curr_price - entry)
            if profit_pips > 3 * sl_pips:
                # move stop loss to BE
                oanda.update_stop_loss(instrument, entry)
            elif profit_pips > 4 * sl_pips:
                # move stop loss to 1:1
                oanda.update_stop_loss(instrument, entry + sl_pips)
            elif profit_pips > 5 * sl_pips:
                # move stop loss to 2:1
                oanda.update_stop_loss(instrument, entry + (2 * sl_pips))
            elif profit_pips > 6 * sl_pips:
                # move stop loss to 3:1
                oanda.update_stop_loss(instrument, entry + (3 * sl_pips))
            elif profit_pips > 7 * sl_pips:
                # move stop loss to 4:1
                oanda.update_stop_loss(instrument, entry + (4 * sl_pips))
            elif profit_pips > 8 * sl_pips:
                # move stop loss to 5:1
                oanda.update_stop_loss(instrument, entry + (5 * sl_pips))
            elif profit_pips > 9 * sl_pips:
                # move stop loss to 6:1
                oanda.update_stop_loss(instrument, entry + (6 * sl_pips))
        # short trade
        else:
            curr_price = oanda.get_current_ask_bid_price(instrument)[0]
            profit_pips = abs(curr_price - entry)
            if profit_pips > 3 * sl_pips:
                # move stop loss to BE
                oanda.update_stop_loss(instrument, entry)
            elif profit_pips > 4 * sl_pips:
                # move stop loss to 1:1
                oanda.update_stop_loss(instrument, entry - sl_pips)
            elif profit_pips > 5 * sl_pips:
                # move stop loss to 2:1
                oanda.update_stop_loss(instrument, entry - (2 * sl_pips))
            elif profit_pips > 6 * sl_pips:
                # move stop loss to 3:1
                oanda.update_stop_loss(instrument, entry - (3 * sl_pips))
            elif profit_pips > 7 * sl_pips:
                # move stop loss to 4:1
                oanda.update_stop_loss(instrument, entry - (4 * sl_pips))
            elif profit_pips > 8 * sl_pips:
                # move stop loss to 5:1
                oanda.update_stop_loss(instrument, entry - (5 * sl_pips))
            elif profit_pips > 9 * sl_pips:
                # move stop loss to 6:1
                oanda.update_stop_loss(instrument, entry - (6 * sl_pips))





#pprint.pprint(trades_list)
#pprint.pprint(orders_list)

manage_trades()
print("Run Successfully --------- " + time.ctime())