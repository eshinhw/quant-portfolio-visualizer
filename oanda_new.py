import os
import json
import pandas as pd
import datetime as dt
from oandapyV20 import API
from typing import List, Dict, Tuple

import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.contrib.requests as requests
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
from demo_credentials import OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID

class Oanda:

    def __init__(self, api_key, accountID) -> None:
        self.client = API(api_key)
        self.acctID = accountID

    def get_balance(self):
        """ Retrieve account balance.

        Args:
            accountID (String): account ID

        Returns:
            Float: current account balance
        """

        resp = self.client.request(accounts.AccountSummary(self.acctID))
        return float(resp["account"]["balance"])

    def get_ohlc(self, symbol: str, count: int, interval: str):
        """ Return historical price data.

        Args:
            symbol (String): symbol
            count (Int): number of intervals
            interval (String): Daily 'D', Weekly 'W', ...

        Returns:
            JSON: json format in python dictionary
        """

        r = instruments.InstrumentsCandles(
            instrument=symbol, params={"count": count,
                            "granularity": interval, "dailyAlignment": 13})
        resp = self.client.request(r)

        data = {"Date": [], "Open": [], "High": [], "Low": [], "Close": []}

        for candle in resp["candles"]:
            data["Date"].append(candle["time"][: candle["time"].index("T")])
            data["Open"].append(float(candle["mid"]["o"]))
            data["High"].append(float(candle["mid"]["h"]))
            data["Low"].append(float(candle["mid"]["l"]))
            data["Close"].append(float(candle["mid"]["c"]))

        df = pd.DataFrame(data)
        df.set_index("Date", inplace=True)
        return df



if __name__ == "__main__":

    oanda = Oanda(OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID)
    print(oanda.get_balance())
    print(oanda.get_ohlc('EUR_USD', 5, 'D'))





