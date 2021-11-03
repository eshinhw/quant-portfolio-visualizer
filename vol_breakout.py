import os
import time
import datetime as dt
from pytz import timezone
from demo_credentials import OANDA_API_KEY, TEST_ACCOUNT_ID
from oandaTrader import OandaTrader
from ta.trend import SMAIndicator
# from fbprophet import Prophet

K = 0.5
INSTRUMENTS = ['EUR_USD']

# Login
if os.name == 'nt':
    oanda = OandaTrader(OANDA_API_KEY, TEST_ACCOUNT_ID)
if os.name == 'posix':
    oanda = OandaTrader(OANDA_API_KEY, TREND_FOLLOWING_ACCOUNT_ID)

INSTRUMENTS = oanda.fx_instruments()

RISK_PER_TRADE = 0.001

ORDERS_LIST = oanda.get_order_list()
TRADES_LIST = oanda.get_trade_list()

SYMBOLS_ORDERS = oanda.symbols_in_orders()
SYMBOLS_TRADES = oanda.symbols_in_trades()

DECIMAL_TABLE = oanda.create_decimal_table()

# def predict(symbol):
#     df = oanda.get_ohlc(symbol,24,'H1')
#     df = df.reset_index()
#     df['ds'] = df['Date']
#     df['y'] = df['Close']
#     data = df[['ds','y']]

#     end_date = get_start_time(symbol) + datetime.timedelta(days=1)

#     model = Prophet()
#     model.fit(data)

#     future = model.make_future_dataframe(periods=30, freq='h')
#     forecast = model.predict(future)
#     predicted_price = forecast[forecast['ds'] == end_date]['yhat']
#     return predicted_price

def open_trades():
    count = 0

    for symbol in INSTRUMENTS:
        count += 1
        print(f"{symbol}\t : \t {count}/{len(INSTRUMENTS)}")
        try:
            df = oanda.get_ohlc(symbol, 5, 'D')
            # print(df)

            now = dt.datetime.now()
            start_time = df.index[-1]
            end_time = start_time + dt.timedelta(days=1)
            # print(start_time)
            # print(now)
            # print(end_time)

            prev_open = df.iloc[-1]['Open']
            prev_high = df.iloc[-1]['High']
            prev_low = df.iloc[-1]['Low']
            prev_close = df.iloc[-1]['Close']
            prev_range = df.iloc[-1]['High'] - df.iloc[-1]['Low']

            long_entry_price = prev_close + (prev_range * K)
            short_entry_price = prev_close - (prev_range * K)

            curr_ask, curr_bid = oanda.get_current_ask_bid_price(symbol)

            # atr = oanda.calculate_ATR(symbol, 20, 'D')

            if symbol not in SYMBOLS_ORDERS and symbol not in SYMBOLS_TRADES:
                # create buy stop order
                oanda.create_stop_order(symbol, long_entry_price, prev_close, RISK_PER_TRADE)
                oanda.create_stop_order(symbol, short_entry_price, prev_close, RISK_PER_TRADE)

            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)

def manage_trades():
    now = dt.datetime.now()
    for trade in TRADES_LIST:
        instrument = trade['instrument']
        open_time = dt.datetime.strptime(trade['openTime'].replace('T', ' ')[:trade['openTime'].index('.')], "%Y-%m-%d %H:%M:%S")
        open_time = open_time - dt.timedelta(hours=4)
        close_time = open_time + dt.timedelta(hours=24)
        if now > close_time:
            oanda.close_open_trade(instrument)

        if instrument in SYMBOLS_ORDERS:
            for order in ORDERS_LIST:
                order_id = order['id']
                if instrument == order['instrument']:
                    oanda.cancel_single_order(order_id)

# Start AutoTrade
# Start Date = 5PM ET
if __name__ == '__main__':
    open_trades()
    manage_trades()