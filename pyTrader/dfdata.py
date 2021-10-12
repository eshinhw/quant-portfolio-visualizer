import oanda
import pandas as pd


def retrieve_ohlc_to_df(symbol: str, period: int, interval: str):
    candles = oanda.get_candle_data(symbol, period + 1, interval)

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


def calculate_ATR(symbol: str, period: int, interval: str):
    df = retrieve_ohlc_to_df(symbol, period, interval)
    # https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python
    # https://stackoverflow.com/questions/35753914/calculating-average-true-range-column-in-pandas-dataframe
    df["RangeOne"] = abs(df["High"] - df["Low"])
    df["RangeTwo"] = abs(df["High"] - df["Close"].shift())
    df["RangeThree"] = abs(df["Close"].shift() - df["Low"])
    df["TrueRange"] = df[["RangeOne", "RangeTwo", "RangeThree"]].max(axis=1)
    df["ATR"] = df["TrueRange"].ewm(span=period).mean()
    return df["ATR"].iloc[-1]


def calculate_prev_min_low(symbol: str, period: int, interval: str):
    df = retrieve_ohlc_to_df(symbol, period, interval)
    df["Low_" + str(period)] = df["Low"].shift(1).rolling(window=period).min()

    return df["Low_" + str(period)].iloc[-1]


def calculate_prev_max_high(symbol: str, period: int, interval: str):
    df = retrieve_ohlc_to_df(symbol, period, interval)
    df["High_" + str(period)
       ] = df["High"].shift(1).rolling(window=period).max()
    return df["High_" + str(period)].iloc[-1]
