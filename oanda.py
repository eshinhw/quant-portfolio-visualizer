import os
import json
import datetime as dt
from oandapyV20 import API
from typing import List, Dict, Tuple
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.contrib.requests as requests
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments


def save_auth():
    with open('./account_info.txt', 'r') as secret:
        contents = secret.readlines()
        auth_dict = {}
        for content in contents:
            splits = content.rstrip('\n').split(':')
            auth_dict[splits[0]] = splits[1]
        secret.close()

    with open('./account_info.json', 'w') as auth:
        json.dump(auth_dict, auth)



def create_sell_limit(account_ID: str,
                      symbol: str,
                      entry: float,
                      stop: float,
                      units: int,
                      trailing_stop: bool) -> None:

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


def create_buy_limit(account_ID: str,
                     symbol: str,
                     entry: float,
                     stop: float,
                     units: int,
                     trailing_stop: bool) -> None:

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


def create_sell_stop(account_ID: str,
                     symbol: str,
                     entry: float,
                     stop: float,
                     units: int,
                     trailing_stop: bool) -> None:

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


def create_buy_stop(account_ID: str,
                    symbol: str,
                    entry: float,
                    stop: float,
                    units: int,
                    trailing_stop: bool) -> None:

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


if os.path.exists('./account_info.json'):
    data = json.load(open('account_info.json', 'r'))
    client = API(access_token=data['token'])
else:
    save_auth()


if __name__ == "__main__":

    with open('./account_info.json', 'r') as fp:
        accounts = json.load(fp)
        client = API(access_token=accounts['token'])
        account_ID = accounts['turtle_soup']
        fp.close()

    cancel_all_orders(account_ID)
