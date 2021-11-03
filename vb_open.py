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

ENTRY_BUFFER = 6

ORDERS_LIST = oanda.get_order_list()
TRADES_LIST = oanda.get_trade_list()

SYMBOLS_ORDERS = oanda.symbols_in_stop_orders()
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

def direction(symbol):

    df = oanda.get_ohlc(symbol, 6, 'D')
    df['strength'] = (df['Close'] - df['Open'])

    bullish = abs(df['strength'].max())
    bearish = abs(df['strength'].min())

    print(df)
    print(bullish, bearish)
    # true -> bullish long, false -> bearish short
    return bullish > bearish



def open_trades():
    #count = 0

    for symbol in INSTRUMENTS:
        #count += 1
        #print(f"{symbol}\t : \t {count}/{len(INSTRUMENTS)}")
        try:
            df = oanda.get_ohlc(symbol, 5, 'D')
            # print(symbol)
            # print(df)

            prev_high = df.iloc[-2]['High']
            prev_low = df.iloc[-2]['Low']
            # prev_close = df.iloc[-2]['Close']
            # prev_range = prev_high - prev_low

            # stop size different depending on market direction: ma
            # optimize entry
            # optimize K
            # prev day candle color

            atr = oanda.calculate_ATR(symbol, 10, 'D')
            #print(prev_range, atr)

            if symbol not in SYMBOLS_ORDERS and symbol not in SYMBOLS_TRADES:
                # if direction(symbol):
                    # bullish -> long at low
                    # weighted_entry = historical_low * 0.6 + prev_low * 0.4
                    # long_entry = weighted_entry + (ENTRY_BUFFER / DECIMAL_TABLE[symbol]['multiple'])
                    long_entry = prev_low + (ENTRY_BUFFER / DECIMAL_TABLE[symbol]['multiple'])
                    sl = long_entry - atr
                    oanda.create_limit_order(symbol, long_entry, sl, RISK_PER_TRADE)
                # else:
                    # bearish -> short at high
                    # weighted_entry = historical_high * 0.6 + prev_high * 0.4
                    # short_entry = weighted_entry -(ENTRY_BUFFER / DECIMAL_TABLE[symbol]['multiple'])
                    short_entry = prev_high - (ENTRY_BUFFER / DECIMAL_TABLE[symbol]['multiple'])
                    sl = short_entry + atr
                    oanda.create_limit_order(symbol, short_entry, sl, RISK_PER_TRADE)

            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)

if __name__ == '__main__':
    open_trades()
    #direction('AUD_CAD')
    print("Open Trades::: " + time.ctime())