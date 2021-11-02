import os
import time
import datetime
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

#INSTRUMENTS = oanda.fx_instruments()

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

# Start AutoTrade
# Start Date = 5PM ET
if __name__ == '__main__':

    for symbol in INSTRUMENTS:
        try:
            df = oanda.get_ohlc(symbol, 5, 'D')
            print(df)

            now = datetime.datetime.now()
            start_time = df.index[-2]
            end_time = start_time + datetime.timedelta(days=1)
            print(start_time)
            print(now)
            print(end_time)

            prev_open = df.iloc[-1]['Open']
            prev_close = df.iloc[-1]['Close']
            prev_high = df.iloc[-1]['High']
            prev_low = df.iloc[-1]['Low']
            prev_range = df.iloc[-1]['High'] - df.iloc[-1]['Low']

            long_entry_price = prev_close + prev_range * K
            short_entry_price = prev_close - prev_range * K

            curr_ask, curr_bid = oanda.get_current_ask_bid_price(symbol)

            # atr = oanda.calculate_ATR(symbol, 20, 'D')

            # open a trade
            if start_time < now < (end_time - datetime.timedelta(seconds=10)):
                # bullish candle
                if curr_ask > long_entry_price:
                    # create buy stop order
                    oanda.create_buy_market_order(symbol, size)
                if curr_bid < short_entry_price:
                    # create sell stop order
                    oanda.create_sell_market_order(symbol, size)


            # close a trade
            else:
                oanda.close_open_trade(symbol)

            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)


