import datetime as dt
from oandapyV20 import API
from typing import List, Dict, Tuple
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments

# /home/pi/Desktop/py-fx-trading-bot/


with open("/home/pi/Desktop/py-fx-trading-bot/oanda_api_token.txt", "r") as auth:
    contents = auth.readlines()
    api_token = contents[0].rstrip("\n")
    client = API(access_token=api_token)
    auth.close()


def cancel_single_order(account_ID: str, order_ID: str) -> None:
    r = orders.OrderCancel(accountID=account_ID, orderID=order_ID)
    client.request(r)


def close_all_trades(account_ID: str) -> None:
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

    Args:
        accountID (String): account ID

    Returns:
        List[String]: open orders
    """
    r = orders.OrderList(account_ID)
    resp = client.request(r)
    return resp["orders"]


def get_trade_list(account_ID: str) -> List[Dict]:
    """ Retrieve a list of open trades

    Args:
        accountID (String): account ID

    Returns:
        List[String]: open trades
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


def get_current_ask_bid_price(symbol: str) -> Tuple[float]:
    """ Return current ask and bid price for pair

    Args:
        pair (String): currency pair

    Returns:
        Tuple: (ask price, bid price)
    """

    r = pricing.PricingInfo(accountID=account_ID,
                            params={"instruments": symbol})
    resp = client.request(r)
    ask_price = float(resp["prices"][0]["closeoutAsk"])
    bid_price = float(resp["prices"][0]["closeoutBid"])
    return (ask_price, bid_price)


def get_current_price(symbol: str) -> float:
    return sum(get_current_ask_bid_price(symbol)) / 2


def create_buy_stop_with_trailing_stop(acct_ID, pair, entry, stop_loss, unit_size):
    trailing_stop = round(abs(entry - stop_loss), 5)
    # print(trailing_stop)
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop_loss)},
            "trailingStopLossOnFill": {
                "timeInForce": "GTC",
                "distance": str(trailing_stop),
            },
            "timeInForce": "GTC",
            "instrument": pair,
            "units": str(unit_size),
            "type": "STOP",
            "positionFill": "DEFAULT",
        }
    }
    r = orders.OrderCreate(acct_ID, data=order_body)
    client.request(r)
    print(
        f"BUY STOP ORDER PLACED | @ {dt.datetime.now()} | pair: {pair} | entry: {str(entry)} | stop_loss: {str(stop_loss)} | unit_size: {str(unit_size)}"
    )


def create_sell_stop_with_trailing_stop(acct_ID, pair, entry, stop_loss, unit_size):
    trailing_stop = round(abs(entry - stop_loss), 5)
    # print(trailing_stop)
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop_loss)},
            "trailingStopLossOnFill": {
                "timeInForce": "GTC",
                "distance": str(trailing_stop),
            },
            "timeInForce": "GTC",
            "instrument": pair,
            "units": "-" + str(unit_size),
            "type": "STOP",
            "positionFill": "DEFAULT",
        }
    }
    r = orders.OrderCreate(acct_ID, data=order_body)
    client.request(r)

    print(
        f"SELL STOP ORDER PLACED | @ {dt.datetime.now()} | pair: {pair} | entry: {str(entry)} | stop_loss: {str(stop_loss)} | unit_size: {str(unit_size)}"
    )


def create_sell_limit_with_trailing_stop(acct_ID, pair, entry, stop_loss, unit_size):
    trailing_stop = round(abs(entry - stop_loss), 5)
    order_body = {
        "order": {
            "price": str(entry),
            "trailingStopLossOnFill": {
                "timeInForce": "GTC",
                "distance": str(trailing_stop),
            },
            "timeInForce": "GTC",
            "instrument": pair,
            "units": "-" + str(unit_size),
            "type": "LIMIT",
            "positionFill": "DEFAULT",
        }
    }
    r = orders.OrderCreate(acct_ID, data=order_body)
    client.request(r)

    print(
        f"SELL LIMIT ORDER PLACED | @ {dt.datetime.now()} | Symbol: {pair} | Entry: {str(entry)} | Trailing Stop: {str(stop_loss)} with {str(trailing_stop)} pips | unit_size: {str(unit_size)}"
    )


def create_sell_limit(acct_ID, pair, entry, stop_loss, unit_size):
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop_loss)},
            "timeInForce": "GTC",
            "instrument": pair,
            "units": "-" + str(unit_size),
            "type": "LIMIT",
            "positionFill": "DEFAULT",
        }
    }
    r = orders.OrderCreate(acct_ID, data=order_body)
    client.request(r)

    print(
        f"SELL LIMIT ORDER PLACED | @ {dt.datetime.now()} | Symbol: {pair} | Entry: {str(entry)} | Stop Loss: {str(stop_loss)} | unit_size: {str(unit_size)}"
    )


def create_buy_limit_with_trailing_stop(acct_ID, pair, entry, stop_loss, unit_size):
    trailing_stop = round(abs(entry - stop_loss), 5)
    order_body = {
        "order": {
            "price": str(entry),
            "trailingStopLossOnFill": {
                "timeInForce": "GTC",
                "distance": str(trailing_stop),
            },
            "timeInForce": "GTC",
            "instrument": pair,
            "units": str(unit_size),
            "type": "LIMIT",
            "positionFill": "DEFAULT",
        }
    }
    r = orders.OrderCreate(acct_ID, data=order_body)
    client.request(r)

    print(
        f"BUY LIMIT ORDER PLACED | @ {dt.datetime.now()} | Symbol: {pair} | Entry: {str(entry)} | Trailing Stop: {str(stop_loss)} with {str(trailing_stop)} pips | unit_size: {str(unit_size)}"
    )


def create_buy_limit(acct_ID, pair, entry, stop_loss, unit_size):
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop_loss)},
            "timeInForce": "GTC",
            "instrument": pair,
            "units": str(unit_size),
            "type": "LIMIT",
            "positionFill": "DEFAULT",
        }
    }
    r = orders.OrderCreate(acct_ID, data=order_body)
    client.request(r)

    print(
        f"BUY LIMIT ORDER PLACED | @ {dt.datetime.now()} | Symbol: {pair} | Entry: {str(entry)} | Stop Loss: {str(stop_loss)} | unit_size: {str(unit_size)}"
    )


if __name__ == "__main__":

    with open("oanda_api_token.txt", "r") as secret:
        contents = secret.readlines()
        api_token = contents[0].rstrip("\n")
        account_ID = contents[1]
        secret.close()

    client = API(access_token=api_token)

    # cancel_all_orders('101-002-5334779-004')

    trade_list = get_trade_list("101-002-5334779-004")

    order_list = get_order_list("101-002-5334779-004")

    for trade in trade_list:
        for order in order_list:
            if order["type"] == "LIMIT" and trade["instrument"] == order["instrument"]:
                cancel_single_order("101-002-5334779-004", order["id"])
                print(
                    f"Order {order['id']} for {trade['instrument']} has been cancelled."
                )
