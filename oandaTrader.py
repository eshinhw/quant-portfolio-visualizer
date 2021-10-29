import os
import json
import pandas as pd
import datetime as dt
from oanda import Oanda
from pprint import pprint
from typing import List, Dict, Tuple
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
from demo_credentials import OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID
from oandapyV20.contrib.requests import MarketOrderRequest, LimitOrderRequest, StopOrderRequest, StopLossOrderRequest

RISK_PER_TRADE = 0.01

class OandaTrader(Oanda):

    def __init__(self, api_key, accountID) -> None:
        super().__init__(api_key, accountID)

    def calculate_unit_size(self,
                            symbol: str,
                            entry: float,
                            stop: float,
                            risk: float):

        # https://www.youtube.com/watch?v=bNEpAOOulwk&ab_channel=KarenFoo

        account_balance = self.get_balance()

        if '_USD' in symbol:
            decimal = 4
            multiple = 10000

            usdcad = self.get_current_ask_bid_price('USD_CAD')[0]
            us_dolloar_per_trade = (account_balance * risk) / usdcad
            entry = round(entry, decimal)
            stop = round(stop, decimal)
            # sl_pips NOT in fractions but in decimal by multiplying multiple
            stop_loss_pips = round(abs(entry - stop), decimal + 1) * multiple
            unit_size = round(us_dolloar_per_trade / stop_loss_pips * multiple, 0)
            return (unit_size, entry, stop, stop_loss_pips)

        if '_JPY' in symbol:
            decimal = 2
            multiple = 100
            cadjpy = self.get_current_ask_bid_price('CAD_JPY')[0]
            jpy_per_trade = (account_balance * risk) * cadjpy
            # risk_amt_per_trade_in_jpy = risk_amt_per_trade /
            entry = round(entry, decimal)
            stop = round(stop, decimal)
            # sl_pips NOT in fractions but in decimal by multiplying multiple
            stop_loss_pips = round(abs(entry - stop), decimal + 1) * multiple
            unit_size = round((jpy_per_trade / stop_loss_pips * multiple), 0)
            print(unit_size)
            return (unit_size, entry, stop, stop_loss_pips)

        if '_CAD' in symbol:
            decimal = 4
            multiple = 10000

            cad_dolloar_per_trade = (account_balance * risk)

            entry = round(entry, decimal)
            stop = round(stop, decimal)
            # sl_pips NOT in fractions but in decimal by multiplying multiple
            stop_loss_pips = round(abs(entry - stop), decimal + 1) * multiple
            unit_size = round(cad_dolloar_per_trade / stop_loss_pips * multiple, 0)
            return (unit_size, entry, stop, stop_loss_pips)



    def update_order_trade_status(self):
        trade_list = self.get_trade_list()
        order_list = self.get_order_list()

        for trade in trade_list:
            for order in order_list:
                if order["type"] == "LIMIT" and trade["instrument"] == order["instrument"]:
                    self.cancel_single_order(order["id"])


    def get_order_details(self, order_ID: str) -> Dict:
        r = orders.OrderDetails(accountID=self.acctID, orderID=order_ID)
        resp = self.client.request(r)
        return (resp['order'])


    def find_order_id(self, symbol: str, direction: str) -> str:
        order_list = self.get_order_list()

        for order in order_list:
            if direction == 'LONG':
                if order['type'] == 'LIMIT' and order['instrument'] == symbol and not ('-' in order['units']):
                    return order['id']
            if direction == 'SHORT':
                if order['type'] == 'LIMIT' and order['instrument'] == symbol and ('-' in order['units']):
                    return order['id']

    def check_open_order(self, symbol: str):
        order_list = self.get_order_list()
        for order in order_list:
            if order["type"] == "LIMIT" and order["instrument"] == symbol:
                return True
        return False

    def check_open_trade(self, symbol: str):
        trade_list = self.get_trade_list()
        for trade in trade_list:
            if trade["instrument"] == symbol:
                return True
        return False

    def close_open_trade(self, symbol: str):
        trade_list = self.get_trade_list()
        for trade in trade_list:
            if trade["instrument"] == symbol:
                r = trades.TradeClose(accountID=self.acctID, tradeID=trade["id"])
                self.client.request(r)


    def cancel_single_order(self, order_ID: str) -> None:
        r = orders.OrderCancel(accountID=self.acctID, orderID=order_ID)
        self.client.request(r)


    def close_all_trades(self) -> None:
        trades_list = self.get_trade_list()
        for trade in trades_list:
            r = trades.TradeClose(accountID=self.acctID, tradeID=trade["id"])
            self.client.request(r)


    def cancel_all_orders(self) -> None:
        order_list = self.get_order_list()
        for order in order_list:
            r = orders.OrderCancel(accountID=self.acctID, orderID=order["id"])
            self.client.request(r)


    def get_order_list(self) -> List[Dict]:
        """ Retrieve a list of open orders
        """
        r = orders.OrderList(self.acctID)
        resp = self.client.request(r)
        return resp['orders']

    def get_trade_list(self) -> List[Dict]:
        """ Retrieve a list of open trades
        """
        r = trades.TradesList(self.acctID)
        resp = self.client.request(r)
        return resp['trades']


    def fx_instruments(self):
        major = ['_USD','_CAD', '_JPY']
        fx_pairs = []
        if os.name == "nt":
            df = pd.read_csv('./instruments.csv')
        if os.name == "posix":
            df = pd.read_csv('/home/eshinhw/pyTrader/instruments.csv')

        df['Instrument'] = df['Instrument'].str.replace('/','_')
        low_spread = df[df['Spread'] < 10].sort_values(by='Spread')
        # print(low_spread.tail(10))
        # print(low_spread)
        # print(df['Instrument'])
        for inst in low_spread['Instrument'].tolist():
            for b in major:
                if b in inst:
                    fx_pairs.append(inst)
        return fx_pairs

    def create_buy_market_order(self, symbol):
        order_body = {
            "order": {
                "type": "MARKET",
                "positionFill": "DEFAULT",
                "instrument": symbol,
                "timeInForce": "FOK",
                "units": "100"
            }
        }

        r = orders.OrderCreate(self.acctID, data=order_body)
        self.client.request(r)


    def create_sell_market_order(self, symbol):
        order_body = {
            "order": {
                "type": "MARKET",
                "positionFill": "DEFAULT",
                "instrument": symbol,
                "timeInForce": "FOK",
                "units": "-100"
            }
        }
        r = orders.OrderCreate(self.acctID, data=order_body)
        self.client.request(r)

    def create_limit_order(self, symbol, entry, stop, risk):
        (units, entry, stop, distance) = self.calculate_unit_size(symbol, entry, stop, risk)
        #print(entry-stop)
        # Sell Limit
        if entry < stop:
            order_body = {
            "order": {
                "price": str(entry),
                "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop)},
                # "trailingStopLossOnFill": {"timeInForce": "GTC", "distance": str(distance)},
                "timeInForce": "GTC",
                "instrument": symbol,
                "units": "-" + str(units),
                "type": "LIMIT",
                "positionFill": "DEFAULT",
                }
            }
            r = orders.OrderCreate(self.acctID, data=order_body)
            self.client.request(r)

        # Buy Limit
        else:
            order_body = {
                "order": {
                    "price": str(entry),
                    "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop)},
                    # "trailingStopLossOnFill": {"timeInForce": "GTC", "distance": str(distance)},
                    "timeInForce": "GTC",
                    "instrument": symbol,
                    "units": str(units),
                    "type": "LIMIT",
                    "positionFill": "DEFAULT",
                }
            }
            r = orders.OrderCreate(self.acctID, data=order_body)
            self.client.request(r)

    def update_stop_loss(self, symbol, new_stop_loss):
        trades_list = self.get_trade_list()

        for trade in trades_list:
            pprint(trade)
            if symbol == trade['instrument']:
                sl_order_id = trade['stopLossOrder']['id']
                trade_id = trade['id']
                # cancel existing stop loss
                self.cancel_single_order(sl_order_id)
                # create new stop loss
                order_body = {
                    "order": {
                        "type": "STOP_LOSS",
                        "tradeID": trade_id,
                        "price": str(new_stop_loss),
                        "timeInForce": "GTC"
                    }
                }
                r = orders.OrderCreate(self.acctID, data=order_body)
                self.client.request(r)


    def create_stop_order(self, symbol, entry, stop):
        units = self.calculate_unit_size(symbol, entry, stop)

        # Sell Stop
        if entry < stop:
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
            r = orders.OrderCreate(self.acctID, data=order_body)
            self.client.request(r)

        else:
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
            r = orders.OrderCreate(self.acctID, data=order_body)
            self.client.request(r)

if __name__ == '__main__':
    ot = OandaTrader(OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID)
    symbol = 'EUR_JPY'
    ot.cancel_all_orders()