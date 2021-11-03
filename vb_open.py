import os
import time
import datetime as dt
from demo_credentials import OANDA_API_KEY, TEST_ACCOUNT_ID, VOLATILITY_BREAKOUT
from oandaTrader import OandaTrader
# from fbprophet import Prophet

K = 0.5

# Login
if os.name == 'nt':
    oanda = OandaTrader(OANDA_API_KEY, VOLATILITY_BREAKOUT)
if os.name == 'posix':
    oanda = OandaTrader(OANDA_API_KEY, VOLATILITY_BREAKOUT)

INSTRUMENTS = oanda.fx_instruments()

RISK_PER_TRADE = 0.0002

ORDERS_LIST = oanda.get_order_list()
TRADES_LIST = oanda.get_trade_list()

SYMBOLS_ORDERS = oanda.symbols_in_stop_orders()
SYMBOLS_TRADES = oanda.symbols_in_trades()

# DECIMAL_TABLE = oanda.create_decimal_table()

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
    #count = 0

    for symbol in INSTRUMENTS:
        #count += 1
        #print(f"{symbol}\t : \t {count}/{len(INSTRUMENTS)}")
        try:
            df = oanda.get_ohlc(symbol, 5, 'D')
            print(symbol)
            # print(df)

            prev_high = df.iloc[-2]['High']
            prev_low = df.iloc[-2]['Low']
            prev_close = df.iloc[-2]['Close']
            prev_range = prev_high - prev_low

            # stop size different depending on market direction: ma
            # optimize entry
            # optimize K
            # prev day candle color

            long_entry_price = prev_close + (prev_range * K)
            short_entry_price = prev_close - (prev_range * K)

            atr = oanda.calculate_ATR(symbol, 20, 'D')
            print(prev_range, atr)

            # if symbol not in SYMBOLS_ORDERS and symbol not in SYMBOLS_TRADES:
            #     # create buy stop order
            #     oanda.create_stop_order(symbol, long_entry_price, prev_close, RISK_PER_TRADE)
            #     oanda.create_stop_order(symbol, short_entry_price, prev_close, RISK_PER_TRADE)

            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)

if __name__ == '__main__':
    open_trades()
    print("Open Trades::: " + time.ctime())