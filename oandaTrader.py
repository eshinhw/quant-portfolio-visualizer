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
from demo_credentials import OANDA_API_KEY, TEST_ACCOUNT_ID
from oandapyV20.contrib.requests import MarketOrderRequest, LimitOrderRequest, StopOrderRequest, StopLossOrderRequest

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
        dec_table = self.create_decimal_table()

        decimal = dec_table[symbol]['decimal']
        multiple = dec_table[symbol]['multiple']

        if '_USD' in symbol:
            usdcad = self.get_current_ask_bid_price('USD_CAD')[0]
            us_dolloar_per_trade = (account_balance * risk) / usdcad
            entry = round(entry, decimal)
            stop = round(stop, decimal)
            # sl_pips NOT in fractions but in decimal by multiplying multiple
            stop_loss_pips = round(abs(entry - stop), decimal + 1) * multiple
            unit_size = round(us_dolloar_per_trade / stop_loss_pips * multiple, 0)
            return (unit_size, entry, stop, stop_loss_pips)

        if '_JPY' in symbol:
            cadjpy = self.get_current_ask_bid_price('CAD_JPY')[0]
            jpy_per_trade = (account_balance * risk) * cadjpy
            # risk_amt_per_trade_in_jpy = risk_amt_per_trade /
            entry = round(entry, decimal)
            stop = round(stop, decimal)
            # sl_pips NOT in fractions but in decimal by multiplying multiple
            stop_loss_pips = round(abs(entry - stop), decimal + 1) * multiple
            unit_size = round((jpy_per_trade / stop_loss_pips * multiple), 0)
            #print(unit_size)
            return (unit_size, entry, stop, stop_loss_pips)

        if '_CAD' in symbol:
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

    def symbols_in_orders(self):
        orders = self.get_order_list()
        symbols = []
        # pprint(orders)
        if orders:
            for order in orders:
                # pprint(order)
                if order['type'] == 'LIMIT' and order['instrument'] not in symbols:
                    symbols.append(order['instrument'])
        return symbols

    def symbols_in_stop_orders(self):
        orders = self.get_order_list()
        symbols = []
        # pprint(orders)
        if orders:
            for order in orders:
                # pprint(order)
                if order['type'] == 'STOP' and order['instrument'] not in symbols:
                    symbols.append(order['instrument'])
        return symbols

    def symbols_in_trades(self):
        trades = self.get_trade_list()
        symbols = []
        #pprint(trades)
        if trades:
            for trade in trades:
                #pprint(trade)
                if trade['instrument'] not in symbols:
                    symbols.append(trade['instrument'])
        return symbols


    def fx_instruments(self):
        quote = ['_USD','_CAD', '_JPY']
        major = ['AUD_', 'USD_', 'NZD_', 'CAD_', 'EUR_']
        quote_pairs = []
        major_pairs = []
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
            for q in quote:
                if q in inst:
                    quote_pairs.append(inst)

        for pair in quote_pairs:
            for m in major:
                if m in pair:
                    major_pairs.append(pair)
        return major_pairs

    def create_decimal_table(self):
        trading_instruments = self.fx_instruments()
        table = {}
        for inst in trading_instruments:
            if '_USD' in inst or '_CAD' in inst:
                table[inst] = {}
                table[inst]['decimal'] = 4
                table[inst]['multiple'] = 10 ** 4
            if '_JPY' in inst:
                table[inst] = {}
                table[inst]['decimal'] = 2
                table[inst]['multiple'] = 10 ** 2
        return table

    def create_buy_market_order(self, symbol, size):
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


    def create_sell_market_order(self, symbol, size):
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
        print(entry-stop)
        print("entry:", entry)
        print('stop:', stop)
        print(entry < stop)
        print(entry > stop)
        # Sell Limit
        if entry < stop:
            print('sell limit')
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
            print(order_body)
            r = orders.OrderCreate(self.acctID, data=order_body)
            self.client.request(r)

        # Buy Limit
        else:
            print('buy limit')
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
            print(order_body)
            r = orders.OrderCreate(self.acctID, data=order_body)
            self.client.request(r)

    def update_stop_loss(self, symbol, new_stop_loss):
        trades_list = self.get_trade_list()

        for trade in trades_list:
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


    def create_stop_order(self, symbol, entry, stop, risk):
        (units, entry, stop, distance) = self.calculate_unit_size(symbol, entry, stop, risk)
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
    ot = OandaTrader(OANDA_API_KEY, TEST_ACCOUNT_ID)
    symbol = 'EUR_JPY'
    ot.cancel_all_orders()
