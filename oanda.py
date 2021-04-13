import json
import datetime as dt
from oandapyV20 import API
from typing import List, Dict, Tuple
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.contrib.requests as requests


# /home/pi/Desktop/py-fx-trading-bot/

with open("oanda_api_token.txt", "r") as auth:
    contents = auth.readlines()
    api_token = contents[0].rstrip("\n")
    client = API(access_token=api_token)
    auth.close()


def calculate_unit_size(account_ID: str,
                        symbol: str,
                        entry: float,
                        stop: float,
                        risk_per_trade: float):

    if '_USD' in symbol:
        decimal = 4
        multiple = 10000

    if '_JPY' in symbol:
        decimal = 2
        multiple = 100

    account_balance = get_acct_balance(account_ID)
    risk_amt_per_trade = account_balance * risk_per_trade
    entry = round(entry, decimal)
    stop = round(stop, decimal)
    stop_loss_pips = round(abs(entry - stop) * multiple, 0)

    if '_USD' in symbol:
        (currentAsk, currentBid) = get_current_ask_bid_price(account_ID, "USD_CAD")
        acct_conversion_rate = 1 / ((currentAsk + currentBid) / 2)
        unit_size = round((risk_amt_per_trade / stop_loss_pips *
                           acct_conversion_rate) * multiple, 0)
        return unit_size

    if '_JPY' in symbol:
        (currentAsk, currentBid) = get_current_ask_bid_price(account_ID, "CAD_JPY")
        acct_conversion_rate = ((currentAsk + currentBid) / 2)
        unit_size = round((risk_amt_per_trade / stop_loss_pips *
                           acct_conversion_rate) * multiple, 0)
        return unit_size


def update_order_trade_status(account_ID: str):

    trade_list = get_trade_list(account_ID)
    order_list = get_order_list(account_ID)

    for trade in trade_list:
        for order in order_list:
            if order["type"] == "LIMIT" and trade["instrument"] == order["instrument"]:
                cancel_single_order(account_ID, order["id"])


def check_open_order(account_ID: str, symbol: str):
    order_list = get_order_list(account_ID)
    for order in order_list:
        if order["type"] == "LIMIT" and order["instrument"] == symbol:
            return True
    return False


def check_open_trade(account_ID: str, symbol: str):
    trade_list = get_trade_list(account_ID)
    for trade in trade_list:
        if trade["instrument"] == symbol:
            return True
    return False


def cancel_single_order(account_ID: str, order_ID: str) -> None:
    """ Cancel a single open order.

    Args:
        account_ID (str): [description]
        order_ID (str): [description]
    """
    r = orders.OrderCancel(accountID=account_ID, orderID=order_ID)
    client.request(r)


def close_all_trades(account_ID: str) -> None:
    """ Close all open trades.

    Args:
        account_ID (str): [description]
    """
    trades_list = get_trade_list(account_ID)
    for trade in trades_list:
        r = trades.TradeClose(accountID=account_ID, tradeID=trade["id"])
        client.request(r)


def cancel_all_orders(account_ID: str) -> None:
    """ Cancel all open orders

    Args:
        accountID (String): account ID
    """
    order_list = get_order_list(account_ID)
    for order in order_list:
        r = orders.OrderCancel(accountID=account_ID, orderID=order["id"])
        client.request(r)


def get_order_list(account_ID: str) -> List[Dict]:
    """ Retrieve a list of open orders
    """
    r = orders.OrderList(account_ID)
    resp = client.request(r)
    return resp["orders"]


def get_trade_list(account_ID: str) -> List[Dict]:
    """ Retrieve a list of open trades
    """
    r = trades.TradesList(account_ID)
    resp = client.request(r)
    return resp["trades"]


def get_acct_balance(account_ID: str) -> float:
    """ Retrieve account balance.

    Args:
        accountID (String): account ID

    Returns:
        Float: current account balance
    """
    resp = client.request(accounts.AccountSummary(account_ID))
    return float(resp["account"]["balance"])


def get_candle_data(symbol: str, count: int, interval: str):
    """ Return historical price data.

    Args:
        symbol (String): symbol
        count (Int): number of intervals
        interval (String): Daily 'D', Weekly 'W', ...

    Returns:
        JSON: json format in python dictionary
    """
    instrument_params = {"count": count,
                         "granularity": interval, "dailyAlignment": 13}

    r = instruments.InstrumentsCandles(
        instrument=symbol, params=instrument_params)
    resp = client.request(r)
    return resp


def calculate_moving_average(symbol: str, period: int, interval: str) -> float:
    instrument_params = {"count": period + 1, "granularity": interval}

    r = instruments.InstrumentsCandles(
        instrument=symbol, params=instrument_params)
    resp = client.request(r)
    closes = []
    for day in resp["candles"]:
        if day["complete"] == True:
            closes.append(float(day["mid"]["c"]))

    return sum(closes) / len(closes)


def get_current_ask_bid_price(account_ID: str, symbol: str) -> Tuple[float]:
    """ Return current ask and bid price for pair

    Args:
        pair (String): currency pair

    Returns:
        Tuple: (ask price, bid price)
    """

    r = pricing.PricingInfo(accountID=account_ID, params={
                            "instruments": symbol})
    resp = client.request(r)
    ask_price = float(resp["prices"][0]["closeoutAsk"])
    bid_price = float(resp["prices"][0]["closeoutBid"])
    return (ask_price, bid_price)


def get_current_price(symbol: str) -> float:
    return sum(get_current_ask_bid_price(account_ID, symbol)) / 2


def create_sell_limit(
        account_ID: str, symbol: str, entry: float, stop: float, units: int, trailing_stop: bool) -> None:

    if trailing_stop is True:
        if "_USD" in symbol:
            dist = round(abs(entry - stop), 5)

        if "_JPY" in symbol:
            dist = round(abs(entry - stop), 3)

        order_body = {
            "order": {
                "price": str(entry),
                "trailingStopLossOnFill": {"timeInForce": "GTC", "distance": str(dist)},
                "timeInForce": "GTC",
                "instrument": symbol,
                "units": "-" + str(units),
                "type": "LIMIT",
                "positionFill": "DEFAULT",
            }
        }

    if trailing_stop is False:
        order_body = {
            "order": {
                "price": str(entry),
                "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop)},
                "timeInForce": "GTC",
                "instrument": symbol,
                "units": "-" + str(units),
                "type": "LIMIT",
                "positionFill": "DEFAULT",
            }
        }
    r = orders.OrderCreate(account_ID, data=order_body)
    client.request(r)


def create_buy_limit(
        account_ID: str, symbol: str, entry: float, stop: float, units: int, trailing_stop: bool) -> None:

    if trailing_stop is True:
        if "_USD" in symbol:
            dist = round(abs(entry - stop), 5)

        if "_JPY" in symbol:
            dist = round(abs(entry - stop), 3)

        order_body = {
            "order": {
                "price": str(entry),
                "trailingStopLossOnFill": {"timeInForce": "GTC", "distance": str(dist)},
                "timeInForce": "GTC",
                "instrument": symbol,
                "units": str(units),
                "type": "LIMIT",
                "positionFill": "DEFAULT",
            }
        }

    if trailing_stop is False:
        order_body = {
            "order": {
                "price": str(entry),
                "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop)},
                "timeInForce": "GTC",
                "instrument": symbol,
                "units": str(units),
                "type": "LIMIT",
                "positionFill": "DEFAULT",
            }
        }
    r = orders.OrderCreate(account_ID, data=order_body)
    client.request(r)


def create_sell_stop(
        account_ID: str, symbol: str, entry: float, stop: float, units: int, trailing_stop: bool) -> None:

    if trailing_stop is True:
        if "_USD" in symbol:
            dist = round(abs(entry - stop), 5)

        if "_JPY" in symbol:
            dist = round(abs(entry - stop), 3)

        order_body = {
            "order": {
                "price": str(entry),
                "trailingStopLossOnFill": {"timeInForce": "GTC", "distance": str(dist)},
                "timeInForce": "GTC",
                "instrument": symbol,
                "units": "-" + str(units),
                "type": "STOP",
                "positionFill": "DEFAULT",
            }
        }

    if trailing_stop is False:
        order_body = {
            "order": {
                "price": str(entry),
                "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop)},
                "timeInForce": "GTC",
                "instrument": symbol,
                "units": "-" + str(units),
                "type": "STOP",
                "positionFill": "DEFAULT",
            }
        }
    r = orders.OrderCreate(account_ID, data=order_body)
    client.request(r)


def create_buy_stop(
        account_ID: str, symbol: str, entry: float, stop: float, units: int, trailing_stop: bool) -> None:

    if trailing_stop is True:
        if "_USD" in symbol:
            dist = round(abs(entry - stop), 5)

        if "_JPY" in symbol:
            dist = round(abs(entry - stop), 3)

        order_body = {
            "order": {
                "price": str(entry),
                "trailingStopLossOnFill": {"timeInForce": "GTC", "distance": str(dist)},
                "timeInForce": "GTC",
                "instrument": symbol,
                "units": str(units),
                "type": "STOP",
                "positionFill": "DEFAULT",
            }
        }

    if trailing_stop is False:
        order_body = {
            "order": {
                "price": str(entry),
                "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop)},
                "timeInForce": "GTC",
                "instrument": symbol,
                "units": str(units),
                "type": "STOP",
                "positionFill": "DEFAULT",
            }
        }
    r = orders.OrderCreate(account_ID, data=order_body)
    client.request(r)


if __name__ == "__main__":

    with open("oanda_api_token.txt", "r") as secret:
        contents = secret.readlines()
        api_token = contents[0].rstrip("\n")
        account_ID = contents[1]
        client = API(access_token=api_token)
        secret.close()

    cancel_all_orders(account_ID)
