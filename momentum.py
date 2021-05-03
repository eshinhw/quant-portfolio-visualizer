import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
from typing import List
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from price import get_historical_monthly_prices

def calculate_equal_weight_momentum(symbol: str, periods: List[int], start_date=None, end_date=None):
    # start_date = dt.datetime(1970,1,1)
    # end_date = dt.datetime.today()
    ret = []
    monthly_prices = get_historical_monthly_prices(symbol)
    for period in periods:
        #print(period)
        monthly_returns = monthly_prices.apply(lambda x: x/x.shift(period) - 1, axis=0)
        monthly_returns = monthly_returns.rename(columns={'Adj_Close': 'Returns'})
        #print(monthly_returns['Returns'].iloc[-1])
        ret.append(monthly_returns['Returns'].iloc[-1])
    #print(ret)
    return sum(ret) / len(ret)

if __name__ == '__main__':
    # global_macro = ['SPY', 'QQQ', 'TLT', 'IEF', 'GLD', 'DBC']
    period = [3,6,12,24,36,48,60,72,84,96,108,120]

    calculate_equal_weight_momentum('abbv', period)

    # data = {'Symbol': [], 'Momentum': []}

    # for symbol in global_macro:
    #     data['Symbol'].append(symbol)
    #     data['Momentum'].append(calculate_equal_weight_momentum(symbol, period))
    # momentum_df = pd.DataFrame(data)
    # momentum_df.set_index('Symbol')
    # momentum_df



