import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
from typing import List
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from price import get_historical_monthly_prices, calculate_periodic_returns

def calculate_equal_weight_momentum(symbol: str, periods: List[int], start_date=None, end_date=None):
    ret = []
    for period in periods:
        returns = calculate_periodic_returns(symbol, period)
        ret.append(returns['Returns'][-1])
    return sum(ret) / len(ret)

if __name__ == '__main__':
    start = dt.datetime(1970,1,1)
    end = dt.datetime.today()

    universe = ['SPY', 'TLT', 'IEF', 'GLD', 'DBC']

    print(calculate_equal_weight_momentum('SPY',[3,6,9,12]))
