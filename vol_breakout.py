import time
import oanda
import schedule
import pandas as pd

# SYMBOL = ["EUR_USD"]
SYMBOLS = ["EUR_USD", "GBP_USD", "AUD_USD", "NZD_USD"]
RISK_PER_TRADE = 0.001
RANGE_K = 0.6
PREV_DAYS = 30

with open("turtle_soup_account_id.txt", "r") as secret:
    contents = secret.readlines()
    account_ID = contents[0]
    secret.close()


def calculate_unit_size(entry, stop_loss):
    """ Calculate unit size per trade (fixed % risk per trade assigned in RISK_PER_TRADE).

    Args:
        entry (Float): entry price
        stop_loss (Float): stop loss price

    Returns:
        Float: unit size
    """
    account_balance = oanda.get_acct_balance(account_ID)
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


def update_order_trade_status():

    trade_list = oanda.get_trade_list(account_ID)
    order_list = oanda.get_order_list(account_ID)

    for trade in trade_list:
        for order in order_list:
            if order["type"] == "LIMIT" and trade["instrument"] == order["instrument"]:
                oanda.cancel_single_order(account_ID, order["id"])
                print(
                    f"Order {order['id']} for {trade['instrument']} has been cancelled."
                )


def retrieve_data(symbol, days):
    candles = oanda.get_candle_data(symbol, days + 1, "D")
    print(candles)

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


def check_trade_conditions():

    for symbol in SYMBOLS:

        prices = retrieve_data(symbol, PREV_DAYS)
        # print(prices)

        # Compute previous day's range
        prev_high = prices["High"].iloc[-2]
        prev_low = prices["Low"].iloc[-2]
        prev_close = prices["Close"].iloc[-2]
        prev_range = prev_high - prev_low
        today_open = prices["Open"].iloc[-1]

        if prev_close > prev_high - (prev_range * 0.1):  # bullish range
            # long breakout entry
            long_price = today_open + (prev_range * RANGE_K)
            oanda.create_buy_stop_with_trailing_stop(
                account_ID,
                symbol,
                long_price,
                today_open,
                calculate_unit_size(long_price, today_open),
            )

        if prev_close < prev_low + (prev_range * 0.1):  # bearish range
            # short breakout entry
            short_price = today_open - (prev_range * RANGE_K)
            oanda.create_sell_stop_with_trailing_stop(
                account_ID,
                symbol,
                short_price,
                today_open,
                calculate_unit_size(short_price, today_open),
            )


if __name__ == "__main__":

    update_order_trade_status()

    schedule.every().friday.at("16:30").do(oanda.cancel_all_orders)

    # while True:
    #     schedule.run_pending()
    #     update_position_status()
    #     turtle_soup_plus_one_condition_check()
    #     time.sleep(5)
