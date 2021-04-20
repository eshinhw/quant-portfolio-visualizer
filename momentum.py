import numpy as np
import pandas as pd
import datetime as dt
from typing import List
import matplotlib.pyplot as plt
import pandas_datareader.data as web


def _convert_monthly_prices(universe: List[str], start_date: dt, end_date: dt):
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

def _calculate_periodic_returns(monthly_prices, period):
    monthly_copy = monthly_prices.copy()
    monthly_copy = monthly_copy.apply(lambda x: x.shift(1)/x.shift(period+1) - 1, axis=0)
    monthly_copy.dropna(inplace=True)
    return monthly_copy

def calculate_equal_weight_momentum(universe: List[str], start_date: dt, end_date: dt, periods: List[int]):
    monthly_prices = _convert_monthly_prices(universe, start_date, end_date)

    momentums = {'Symbol': []}

    for period in periods:
        returns = _calculate_periodic_returns(monthly_prices, period)
        momentums[f'{str(period)}M_Return'] = []
        for symbol in list(monthly_prices.columns):
            if symbol not in momentums['Symbol']:
                momentums['Symbol'].append(symbol)
            momentums[f'{str(period)}M_Return'].append(returns[symbol].iloc[-1])

    momentum_df = pd.DataFrame(momentums)
    momentum_df.set_index('Symbol', inplace=True)
    momentum_df['EW_MOMENTUM'] = momentum_df.mean(axis=1)
    momentum_df.sort_values(by='EW_MOMENTUM', inplace=True, ascending=False)
    return momentum_df


if __name__ == '__main__':
    start = dt.datetime(1970,1,1)
    end = dt.datetime.today()

    universe = ['SPY', 'TLT', 'IEF', 'GLD', 'DBC']

    #print(web.DataReader('DBC', 'yahoo', start, end)['Adj Close'])
    # df = _convert_monthly_prices(universe, start, end)
    # print(df)
    # mom = _calculate_periodic_returns(df, 3)
    # print(mom['DBC'].iloc[-1])
    # print(df)
    # print(df.loc['DBC', -2])
    print(calculate_equal_weight_momentum(universe, start, end, [1,3,6,12]))