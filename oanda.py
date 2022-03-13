import pandas as pd
import datetime as dt
from oandapyV20 import API
from pprint import pprint
from typing import List, Dict, Tuple
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades


class Oanda:

    def __init__(self, api_key, accountID) -> None:
        self.client = API(api_key)
        self.acctID = accountID

    def get_balance(self):
        resp = self.client.request(accounts.AccountSummary(self.acctID))
        return float(resp["account"]["balance"])

    def get_ohlc(self, symbol: str, count: int, interval: str):
        r = instruments.InstrumentsCandles(instrument=symbol, params={"count": count, "granularity": interval})
        resp = self.client.request(r)

        data = {"Date": [], "Open": [], "High": [], "Low": [], "Close": []}

        for candle in resp["candles"]:
            date = candle['time'].replace('T', ' ')[:candle['time'].index('.')]
            data["Date"].append(dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
            data["Open"].append(float(candle["mid"]["o"]))
            data["High"].append(float(candle["mid"]["h"]))
            data["Low"].append(float(candle["mid"]["l"]))
            data["Close"].append(float(candle["mid"]["c"]))

        df = pd.DataFrame(data)
        df.set_index("Date", inplace=True)
        return df

    def get_current_low(self, symbol, count, interval):
        r = instruments.InstrumentsCandles(instrument=symbol,
                                           params={"count": count,
                                                    "granularity": interval,
                                                    "dailyAlignment": 17})
        resp = self.client.request(r)
        most_recent_low = float(resp['candles'][-1]['mid']['l'])
        return most_recent_low

    def get_current_high(self, symbol, count, interval):
        r = instruments.InstrumentsCandles(instrument=symbol,
                                           params={"count": count,
                                                    "granularity": interval,
                                                    "dailyAlignment": 17})
        resp = self.client.request(r)
        most_recent_high = float(resp['candles'][-1]['mid']['h'])
        return most_recent_high


    def get_current_ask_bid_price(self, symbol: str) -> Tuple[float]:
        r = pricing.PricingInfo(accountID=self.acctID,
                                params={"instruments": symbol})
        resp = self.client.request(r)
        ask_price = float(resp["prices"][0]["closeoutAsk"])
        bid_price = float(resp["prices"][0]["closeoutBid"])
        return (ask_price, bid_price)

    def calculate_MA(self, symbol: str, period: int, interval: str):
        df = self.get_ohlc(symbol, period + 3, interval)
        ma = df['Close'].rolling(period).mean().iloc[-1]
        return ma

    def calculate_ATR(self, symbol: str, period: int, interval: str):
        df = self.get_ohlc(symbol, period + 3, interval)
        # https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python
        # https://stackoverflow.com/questions/35753914/calculating-average-true-range-column-in-pandas-dataframe
        df["RangeOne"] = abs(df["High"] - df["Low"])
        df["RangeTwo"] = abs(df["High"] - df["Close"].shift())
        df["RangeThree"] = abs(df["Close"].shift() - df["Low"])
        df["TrueRange"] = df[["RangeOne", "RangeTwo", "RangeThree"]].max(axis=1)
        df["ATR"] = df["TrueRange"].ewm(span=period).mean()
        return df["ATR"].iloc[-1]

    def calculate_prev_min_low(self, symbol: str, period: int, interval: str):
        df = self.get_ohlc(symbol, period, interval)
        return min(df['Low'])

    def calculate_prev_max_high(self, symbol: str, period: int, interval: str):
        df = self.get_ohlc(symbol, period, interval)
        return max(df['High'])

    def calculate_unit_size(self,
                            symbol: str,
                            entry: float,
                            stop: float,
                            risk: float):

        # https://www.youtube.com/watch?v=bNEpAOOulwk&ab_channel=KarenFoo

        account_balance = self.get_balance()
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
        while trades_list:
            for trade in trades_list:
                r = trades.TradeClose(accountID=self.acctID, tradeID=trade["id"])
                self.client.request(r)
            trades_list = self.get_trade_list()

    def cancel_all_orders(self) -> None:
        order_list = self.get_order_list()
        while order_list:
            for order in order_list:
                r = orders.OrderCancel(accountID=self.acctID, orderID=order["id"])
                self.client.request(r)
            order_list = self.get_order_list()


    def get_order_list(self) -> List[Dict]:
        """ Retrieve a list of open orders"""
        r = orders.OrderList(self.acctID)
        resp = self.client.request(r)
        return resp['orders']

    def get_trade_list(self) -> List[Dict]:
        """ Retrieve a list of open trades"""
        r = trades.TradesList(self.acctID)
        resp = self.client.request(r)
        return resp['trades']

    def symbols_in_orders(self):
        orders = self.get_order_list()
        symbols = []
        #pprint(orders)
        if orders:
            for order in orders:
                #pprint(order)
                if order['type'] != 'STOP_LOSS' and order['instrument'] not in symbols:
                    #print(order['instrument'])
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

    def create_limit_order(self, symbol, entry, stop, risk):
        (units, entry, stop, distance) = self.calculate_unit_size(symbol, entry, stop, risk)
        # print(entry-stop)
        # print("entry:", entry)
        # print('stop:', stop)
        # print(entry < stop)
        # print(entry > stop)
        # Sell Limit
        if entry < stop:
            #print('sell limit')
            order_body = {
            "order": {
                "price": str(entry),
                "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop)},
                "trailingStopLossOnFill": {"timeInForce": "GTC", "distance": str(distance)},
                "timeInForce": "GTC",
                "instrument": symbol,
                "units": "-" + str(units),
                "type": "LIMIT",
                "positionFill": "DEFAULT",
                }
            }
            #print(order_body)
            r = orders.OrderCreate(self.acctID, data=order_body)
            self.client.request(r)

        # Buy Limit
        else:
            #print('buy limit')
            order_body = {
                "order": {
                    "price": str(entry),
                    "stopLossOnFill": {"timeInForce": "GTC", "price": str(stop)},
                    "trailingStopLossOnFill": {"timeInForce": "GTC", "distance": str(distance)},
                    "timeInForce": "GTC",
                    "instrument": symbol,
                    "units": str(units),
                    "type": "LIMIT",
                    "positionFill": "DEFAULT",
                }
            }
            #print(order_body)
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

if __name__ == "__main__":
    od = Oanda()




