import time
import oanda
import schedule
import pandas as pd

# SYMBOLS = ["EUR_USD"]
#SYMBOLS = ["EUR_USD", "GBP_USD", "AUD_USD", 'NZD_USD', 'USD_JPY', 'GBP_JPY']
SYMBOLS = ['USD_JPY', 'GBP_JPY']
RISK_PER_TRADE = 0.001

PREV_DAYS = 30
ENTRY_PIP_BUFF = 0.0007
ATR_SL_MULTIPLE = 1

# /home/pi/Desktop/py-fx-trading-bot/

# with open("turtle_soup_account_id.txt", "r") as secret:
#     contents = secret.readlines()
#     account_ID = contents[0]
#     secret.close()

account_ID = '101-002-5334779-003'


def update_order_trade_status():

    trade_list = oanda.get_trade_list(account_ID)
    order_list = oanda.get_order_list(account_ID)

    for trade in trade_list:
        for order in order_list:
            if order["type"] == "LIMIT" and trade["instrument"] == order["instrument"]:
                oanda.cancel_single_order(account_ID, order["id"])


def check_open_order(symbol):
    order_list = oanda.get_order_list(account_ID)
    # print(order_list)
    for order in order_list:
        if order["type"] == "LIMIT" and order["instrument"] == symbol:
            return True

    return False


def check_open_trade(symbol):
    trade_list = oanda.get_trade_list(account_ID)
    for trade in trade_list:
        if trade["instrument"] == symbol:
            return True

    return False


def retrieve_data(symbol, days):
    candles = oanda.get_candle_data(symbol, days + 1, "D")

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
    df["High_" + str(days)] = df["High"].shift(1).rolling(window=days).max()

    return df["High_" + str(days)].iloc[-1]


def short_entry(df, symbol, days):
    df = df.copy()
    df["Low_" + str(days)] = df["Low"].shift(1).rolling(window=days).min()

    return df["Low_" + str(days)].iloc[-1]


def prev_low(df, symbol, days):  # place to go long
    df = df.copy()
    df["Low_" + str(days)] = df["Low"].shift(1).rolling(window=days).min()

    return df["Low_" + str(days)].iloc[-1]


def prev_high(df, symbol, days):  # place to go short
    df = df.copy()
    df["High_" + str(days)] = df["High"].shift(1).rolling(window=days).max()
    return df["High_" + str(days)].iloc[-1]


def place_orders(symbol: str):

    decimal = 5

    if "_USD" in symbol:
        decimal = 5
    if "_JPY" in symbol:
        decimal = 3

    # retrieve price data
    df = retrieve_data(symbol, PREV_DAYS)
    # entry prices
    long_entry_price = round(
        prev_low(df, symbol, PREV_DAYS) + ENTRY_PIP_BUFF, decimal)
    short_entry_price = round(
        prev_high(df, symbol, PREV_DAYS) - ENTRY_PIP_BUFF, decimal)

    stop_loss = calculate_ATR(df, symbol, PREV_DAYS) * ATR_SL_MULTIPLE
    long_sl = round(long_entry_price - stop_loss, decimal)
    short_sl = round(short_entry_price + stop_loss, decimal)

    if (not check_open_order(symbol)) and (not check_open_trade(symbol)):
        oanda.create_buy_limit(
            account_ID,
            symbol,
            long_entry_price,
            long_sl,
            oanda.calculate_unit_size(
                account_ID, symbol, long_entry_price, long_sl, RISK_PER_TRADE),
            True,
        )

        oanda.create_sell_limit(
            account_ID,
            symbol,
            short_entry_price,
            short_sl,
            oanda.calculate_unit_size(account_ID, symbol,
                                      short_entry_price, short_sl, RISK_PER_TRADE),
            True,
        )


def check_trade_conditions():
    for symbol in SYMBOLS:
        place_orders(symbol)


if __name__ == "__main__":

    update_order_trade_status()
    check_trade_conditions()
