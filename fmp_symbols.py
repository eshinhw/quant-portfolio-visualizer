import pprint
import requests
import calendar
import numpy as np
import pandas as pd
import datetime as dt
from typing import List
from credentials import FMP_API_KEY

START_DATE = dt.datetime(1970, 1, 1)
END_DATE = dt.datetime.today()

def sp500_symbols():
    symbols = []
    data = requests.get(f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={FMP_API_KEY}").json()

    for d in data:
        symbols.append(d["symbol"])

    return symbols


def dow_symbols():
    symbols = []
    data = requests.get(f"https://financialmodelingprep.com/api/v3/dowjones_constituent?apikey={FMP_API_KEY}").json()

    for d in data:
        symbols.append(d["symbol"])

    return symbols

def crypto_symbols():
    cryptos = []
    data = requests.get(f"https://financialmodelingprep.com/api/v3/quotes/crypto?apikey={FMP_API_KEY}").json()

    for d in data:
        cryptos.append(d['symbol'])

    return cryptos