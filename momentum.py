import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
from typing import List
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from price import convert_monthly_prices, calculate_periodic_returns

def calculate_equal_weight_momentum(symbols: str or List[str], start_date: dt, end_date: dt, periods: List[int]):
    monthly_prices = convert_monthly_prices(symbols, start_date, end_date)
    momentums = {'Symbol': [], 'Name': []}

    for period in periods:
        returns = calculate_periodic_returns(monthly_prices, period)
        momentums[f'{str(period)}M_Return'] = []
        for symbol in list(monthly_prices.columns):
            if symbol not in momentums['Symbol']:
                momentums['Symbol'].append(symbol)
                momentums['Name'].append(yf.Ticker(symbol).info['shortName'])
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
    print(convert_monthly_prices('MMM', start, end))
    #print(calculate_equal_weight_momentum(universe, start, end, [1,3,6,12]))