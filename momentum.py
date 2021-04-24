import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
from typing import List
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from price import get_historical_monthly_prices, calculate_periodic_returns

def calculate_equal_weight_momentum(symbol: str, periods: List[int], start_date=None, end_date=None):
    start_date = dt.datetime(1970,1,1)
    end_date = dt.datetime.today()
    ret = []
    for period in periods:
        returns = calculate_periodic_returns(symbol, period)
        ret.append(returns['Returns'][-1])
    return sum(ret) / len(ret)

if __name__ == '__main__':
    global_macro = ['SPY', 'QQQ', 'TLT', 'IEF', 'GLD', 'DBC']
    period = [1,3,6,12,24,36,48,60]

    data = {'Symbol': [], 'Momentum': []}

    for symbol in global_macro:
        print(symbol)
        data['Symbol'].append(symbol)
        data['Momentum'].append(calculate_equal_weight_momentum(symbol, period))
    momentum_df = pd.DataFrame(data)
    momentum_df.set_index('Symbol')
    momentum_df
