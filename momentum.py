import numpy as np
import pandas as pd
import datetime as dt
from typing import List
import matplotlib.pyplot as plt
import pandas_datareader.data as web


def convert_monthly_prices(universe: List[str], start_date: str, end_date: str):
    prices = pd.DataFrame()
    for asset in universe:
        prices[asset] = web.DataReader(asset, 'yahoo', start_date, end_date)['Adj Close']
    prices.dropna(inplace=True)
    prices.reset_index(inplace=True)
    prices['STD_YM'] = prices['Date'].map(lambda x : dt.datetime.strftime(x, '%Y-%m'))
    month_list = prices['STD_YM'].unique()
    monthly_prices = pd.DataFrame()
    for m in month_list:
        monthly_prices = monthly_prices.append(prices[prices['STD_YM'] == m].iloc[-1,:])
    monthly_prices = monthly_prices.drop(columns=['STD_YM'], axis=1)
    monthly_prices.set_index('Date', inplace=True)
    return monthly_prices
