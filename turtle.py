import oanda
import pandas as pd
from oanda import get_candle_data, get_current_ask_price, get_current_bid_price

INSTRUMENTS = ["EUR_USD", "GBP_USD", "AUD_USD", "NZD_USD"]


def retrieve_data(symbol, days):
    candles = get_candle_data(symbol, days + 1, "D")

    data_dict = {"Date": [], "Open": [], "High": [], "Low": [], "Close": []}

    for candle in candles["candles"]:
        data_dict["Date"].append(candle["time"][: candle["time"].index("T")])
        data_dict["Open"].append(float(candle["mid"]["o"]))
        data_dict["High"].append(float(candle["mid"]["h"]))
        data_dict["Low"].append(float(candle["mid"]["l"]))
        data_dict["Close"].append(float(candle["mid"]["c"]))

    df = pd.DataFrame(data_dict)
    df.set_index("Date", inplace=True)
    return df


def calculate_ATR(df, symbol, days):
    df = df.copy()
    # https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python
    # https://stackoverflow.com/questions/35753914/calculating-average-true-range-column-in-pandas-dataframe
    df["RangeOne"] = abs(df["High"] - df["Low"])
    df["RangeTwo"] = abs(df["High"] - df["Close"].shift())
    df["RangeThree"] = abs(df["Close"].shift() - df["Low"])
    df["TrueRange"] = df[["RangeOne", "RangeTwo", "RangeThree"]].max(axis=1)
    df["ATR"] = df["TrueRange"].ewm(span=days).mean()
    return df["ATR"].iloc[-1]


def long_entry(df, symbol, days):
    df = df.copy()
    df['High_' + str(days)] = df['High'].shift(1).rolling(window=days).max()

    return df['High_' + str(days)].iloc[-1]


def short_entry(df, symbol, days):
    df = df.copy()
    df['Low_' + str(days)] = df['Low'].shift(1).rolling(window=days).min()

    return df['Low_' + str(days)].iloc[-1]

# def long_exit(symbol, days):
#     df = _retrieve_data(symbol, days)
#     df['Low_' + str(days)] = df['Low'].shift(1).rolling(window=days).min()

#     return df['Low_' + str(days)].iloc[-1]


# def short_exit(symbol, days):
#     df = _retrieve_data(symbol, days)
#     df['High_' + str(days)] = df['High'].shift(1).rolling(window=days).max()

#     return df['High_' + str(days)].iloc[-1]


if __name__ == "__main__":

    for symbol in INSTRUMENTS:
        # retrieve price data
        df = retrieve_data(symbol, 55)
        # entry prices
        long_entry_price = long_entry(df, symbol, 55)
        short_entry_price = short_entry(df, symbol, 55)

        # stops
        TwoATR = 2 * calculate_ATR(df, symbol, 20)
        long_stop_loss = round(long_entry_price - TwoATR, 5)
        short_stop_loss = round(short_entry_price + TwoATR, 5)

        # current prices
        current_ask = get_current_ask_price(symbol)
        current_bid = get_current_bid_price(symbol)

        oanda.cancel_all_orders()

        # place entry orders
        # if current_ask < short_entry_price:
        # units = oanda.calculate_unit_size(current_ask, long_stop_loss)
        # oanda.create_sell_limit(
        #     symbol, current_ask, short_stop_loss, units)
        # # if current_bid > long_entry_price:
        # units = oanda.calculate_unit_size(current_bid, short_stop_loss)
        # oanda.create_sell_limit(
        #     symbol, current_bid, short_stop_loss, units)
