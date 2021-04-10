import datetime as dt
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments

with open("oanda_demo_api_token.txt", "r") as secret:
    contents = secret.readlines()
    api_token = contents[0].rstrip("\n")
    account_ID = contents[1]
    secret.close()

client = API(access_token=api_token)


def cancel_single_order(order_ID):
    r = orders.OrderCancel(accountID=account_ID, orderID=order_ID)
    client.request(r)


def close_all_trades():
    trades_list = get_trade_list()
    for trade in trades_list:
        r = trades.TradeClose(accountID=account_ID, tradeID=trade["id"])
        client.request(r)
    print("All open trades are CLOSED.")


def cancel_all_orders():
    """ Cancel all open orders

    Args:
        accountID (String): account ID
    """
    order_list = get_order_list()
    for order in order_list:
        r = orders.OrderCancel(accountID=account_ID, orderID=order["id"])
        client.request(r)
    print("All open orders are CANCELLED.")


def get_order_list():
    """ Retrieve a list of open orders

    Args:
        accountID (String): account ID

    Returns:
        List[String]: open orders
    """
    r = orders.OrderList(account_ID)
    resp = client.request(r)
    return resp["orders"]


def get_trade_list():
    """ Retrieve a list of open trades

    Args:
        accountID (String): account ID

    Returns:
        List[String]: open trades
    """
    r = trades.TradesList(account_ID)
    resp = client.request(r)
    # print("RESPONSE:\n{}".format(json.dumps(resp, indent=2)))
    return resp["trades"]


def get_acct_balance():
    """ Retrieve account balance.

    Args:
        accountID (String): account ID

    Returns:
        Float: current account balance
    """
    resp = client.request(accounts.AccountSummary(account_ID))
    return float(resp["account"]["balance"])


def get_candle_data(symbol, count, interval):
    """ Return historical price data.

    Args:
        symbol (String): symbol
        count (Int): number of intervals
        interval (String): Daily 'D', Weekly 'W', ...

    Returns:
        JSON: json format in python dictionary
    """
    instrument_params = {"count": count, "granularity": interval}

    r = instruments.InstrumentsCandles(
        instrument=symbol, params=instrument_params)
    resp = client.request(r)
    return resp


def calculate_moving_average(symbol, count, interval):
    instrument_params = {"count": count + 1, "granularity": interval}

    r = instruments.InstrumentsCandles(
        instrument=symbol, params=instrument_params)
    resp = client.request(r)
    closes = []
    for day in resp["candles"]:
        if day["complete"] == True:
            closes.append(float(day["mid"]["c"]))

    return sum(closes) / len(closes)


def get_current_ask_bid_price(pair):
    """ Return current ask and bid price for pair

    Args:
        pair (String): currency pair

    Returns:
        Tuple: (ask price, bid price)
    """

    r = pricing.PricingInfo(accountID=account_ID, params={"instruments": pair})
    resp = client.request(r)
    ask_price = float(resp["prices"][0]["closeoutAsk"])
    bid_price = float(resp["prices"][0]["closeoutBid"])
    return (ask_price, bid_price)


def get_current_price(pair):
    return sum(get_current_ask_bid_price(pair)) / 2


def create_buy_stop(pair, entry, stop_loss, unit_size, trailing_stop=0):
    # trailing_stop = round(abs(entry - stop_loss), 5)
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop_loss)},
            "trailingStopLossOnFill": {
                "timeInForce": "GTC",
                "distance": str(trailing_stop)
            },
            "timeInForce": "GTC",
            "instrument": pair,
            "units": str(unit_size),
            "type": "STOP",
            "positionFill": "DEFAULT"
        }
    }
    r = orders.OrderCreate(account_ID, data=order_body)
    client.request(r)
    print(
        f"BUY STOP ORDER PLACED | @ {dt.datetime.now()} | pair: {pair} | entry: {str(entry)} | stop_loss: {str(stop_loss)} | unit_size: {str(unit_size)}"
    )


def create_sell_stop(pair, entry, stop_loss, unit_size, trailing_stop=0):
    # trailing_stop = round(abs(entry - stop_loss), 5)
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop_loss)},
            "trailingStopLossOnFill": {
                "timeInForce": "GTC",
                "distance": str(trailing_stop)
            },
            "timeInForce": "GTC",
            "instrument": pair,
            "units": "-" + str(unit_size),
            "type": "STOP",
            "positionFill": "DEFAULT"
        }
    }
    r = orders.OrderCreate(account_ID, data=order_body)
    client.request(r)

    print(
        f"SELL STOP ORDER PLACED | @ {dt.datetime.now()} | pair: {pair} | entry: {str(entry)} | stop_loss: {str(stop_loss)} | unit_size: {str(unit_size)}"
    )


def create_sell_limit_with_trailing_stop(pair, entry, stop_loss, unit_size):
    trailing_stop = round(abs(entry - stop_loss), 5)
    order_body = {
        "order": {
            "price": str(entry),
            "trailingStopLossOnFill": {
                "timeInForce": "GTC",
                "distance": str(trailing_stop)
            },
            "timeInForce": "GTC",
            "instrument": pair,
            "units": "-" + str(unit_size),
            "type": "LIMIT",
            "positionFill": "DEFAULT"
        }
    }
    r = orders.OrderCreate(account_ID, data=order_body)
    client.request(r)

    print(
        f"SELL LIMIT ORDER PLACED | @ {dt.datetime.now()} | Symbol: {pair} | Entry: {str(entry)} | Trailing Stop: {str(stop_loss)} with {str(trailing_stop)} pips | unit_size: {str(unit_size)}"
    )


def create_sell_limit(pair, entry, stop_loss, unit_size):
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop_loss)},
            "timeInForce": "GTC",
            "instrument": pair,
            "units": "-" + str(unit_size),
            "type": "LIMIT",
            "positionFill": "DEFAULT"
        }
    }
    r = orders.OrderCreate(account_ID, data=order_body)
    client.request(r)

    print(
        f"SELL LIMIT ORDER PLACED | @ {dt.datetime.now()} | Symbol: {pair} | Entry: {str(entry)} | Stop Loss: {str(stop_loss)} | unit_size: {str(unit_size)}"
    )


def create_buy_limit_with_trailing_stop(pair, entry, stop_loss, unit_size):
    trailing_stop = round(abs(entry - stop_loss), 5)
    order_body = {
        "order": {
            "price": str(entry),
            "trailingStopLossOnFill": {
                "timeInForce": "GTC",
                "distance": str(trailing_stop)
            },
            "timeInForce": "GTC",
            "instrument": pair,
            "units": str(unit_size),
            "type": "LIMIT",
            "positionFill": "DEFAULT"
        }
    }
    r = orders.OrderCreate(account_ID, data=order_body)
    client.request(r)

    print(
        f"BUY LIMIT ORDER PLACED | @ {dt.datetime.now()} | Symbol: {pair} | Entry: {str(entry)} | Trailing Stop: {str(stop_loss)} with {str(trailing_stop)} pips | unit_size: {str(unit_size)}"
    )


def create_buy_limit(pair, entry, stop_loss, unit_size):
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop_loss)},
            "timeInForce": "GTC",
            "instrument": pair,
            "units": str(unit_size),
            "type": "LIMIT",
            "positionFill": "DEFAULT"
        }
    }
    r = orders.OrderCreate(account_ID, data=order_body)
    client.request(r)

    print(
        f"BUY LIMIT ORDER PLACED | @ {dt.datetime.now()} | Symbol: {pair} | Entry: {str(entry)} | Stop Loss: {str(stop_loss)} | unit_size: {str(unit_size)}"
    )


if __name__ == '__main__':

    with open("oanda_demo_api_token.txt", "r") as secret:
        contents = secret.readlines()
        api_token = contents[0].rstrip("\n")
        account_ID = contents[1]
        secret.close()

    client = API(access_token=api_token)

    resp = client.request(accounts.AccountSummary(account_ID))
    print(float(resp["account"]["balance"]))

    # r = orders.OrderList(account_ID)
    # resp = client.request(r)
    # print(resp["orders"])

    r = trades.TradesList(account_ID)
    resp = client.request(r)
    # print("RESPONSE:\n{}".format(json.dumps(resp, indent=2)))
    print(resp["trades"])
