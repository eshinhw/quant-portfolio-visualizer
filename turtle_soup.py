import time
import oanda
import schedule
import pandas as pd
import dfdata

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


def check_condition_and_place_orders(symbol: str):

    for symbol in SYMBOLS:

        decimal = 5

        if "_USD" in symbol:
            decimal = 5
        if "_JPY" in symbol:
            decimal = 3

        # entry prices
        long_entry_price = round(
            dfdata.calculate_prev_min_low(symbol, PREV_DAYS, 'D') + ENTRY_PIP_BUFF, decimal)
        short_entry_price = round(
            dfdata.calculate_prev_max_high(symbol, PREV_DAYS, 'D') - ENTRY_PIP_BUFF, decimal)

        stop_loss = dfdata.calculate_ATR(
            symbol, PREV_DAYS, 'D') * ATR_SL_MULTIPLE
        long_sl = round(long_entry_price - stop_loss, decimal)
        short_sl = round(short_entry_price + stop_loss, decimal)

        if (not oanda.check_open_order(account_ID, symbol)) and (not oanda.check_open_trade(account_ID, symbol)):
            oanda.create_buy_limit(
                account_ID=account_ID,
                symbol=symbol,
                entry=long_entry_price,
                stop=long_sl,
                units=oanda.calculate_unit_size(
                    account_ID, symbol, long_entry_price, long_sl, RISK_PER_TRADE),
                trailing_stop=True,
            )

            oanda.create_sell_limit(
                account_ID=account_ID,
                symbol=symbol,
                entry=short_entry_price,
                stop=short_sl,
                units=oanda.calculate_unit_size(account_ID, symbol,
                                                short_entry_price, short_sl, RISK_PER_TRADE),
                trailing_stop=True,
            )


if __name__ == "__main__":

    oanda.update_order_trade_status(account_ID)
    check_condition_and_place_orders()
