import time
import oanda
import schedule
import pandas as pd


INSTRUMENTS = ["EUR_USD", "GBP_USD", "AUD_USD", "NZD_USD"]
RISK_PER_TRADE = 0.001
POSITION_STATUS = {}


def calculate_unit_size(entry, stop_loss):
    """ Calculate unit size per trade (fixed % risk per trade assigned in RISK_PER_TRADE).

    Args:
        entry (Float): entry price
        stop_loss (Float): stop loss price

    Returns:
        Float: unit size
    """
    account_balance = oanda.get_acct_balance()
    risk_amt_per_trade = account_balance * RISK_PER_TRADE
    entry = round(entry, 4)
    stop_loss = round(stop_loss, 4)
    stop_loss_pips = round(abs(entry - stop_loss) * 10000, 0)
    (currentAsk, currentBid) = oanda.get_current_ask_bid_price("USD_CAD")
    acct_conversion_rate = 1 / ((currentAsk + currentBid) / 2)
    unit_size = round(
        (risk_amt_per_trade / stop_loss_pips * acct_conversion_rate) * 10000, 0
    )
    return unit_size


def update_position_status(pair):

    trades_list = oanda.get_trade_list()
    open_trades_inst = []
    for trade in trades_list:
        open_trades_inst.append(trade["instrument"])
    for pair in INSTRUMENTS:

        if (
            pair in POSITION_STATUS.keys()
            and POSITION_STATUS[pair] == 1
            and not (pair in open_trades_inst)
        ):
            POSITION_STATUS[pair] = 0


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


# def long_exit(symbol, days):
#     df = _retrieve_data(symbol, days)
#     df['Low_' + str(days)] = df['Low'].shift(1).rolling(window=days).min()
# df['High_' + str(days)] = df['High'].shift(1).rolling(window=days).max()

#     return df['Low_' + str(days)].iloc[-1]

def entry_check():
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
        current_price = oanda.get_current_price(symbol)

        # place entry orders
        if current_price < short_entry_price:
            units = calculate_unit_size(current_price, long_stop_loss)
            oanda.create_sell_limit(
                symbol, current_price, short_stop_loss, units)
        if current_price > long_entry_price:
            units = calculate_unit_size(current_price, short_stop_loss)
            oanda.create_buy_limit(symbol, current_price,
                                   short_stop_loss, units)


if __name__ == "__main__":
    # oanda.close_all_trades()
    # oanda.cancel_all_orders()

    # run execute every 4 hours
    schedule.every().day.at("21:01").do(oanda.cancel_all_orders)

    while True:
        schedule.run_pending()
        time.sleep(1)
