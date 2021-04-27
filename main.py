import os
import math
import price
import ratios
import requests
import momentum
import pyticker
import dividend
import questrade
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from qtrade import Questrade as qt
import pandas_datareader.data as web

# ## Global Macro Momentum

global_macro = ['SPY', 'QQQ', 'TLT', 'IEF', 'GLD', 'DBC']
period = [3,6,12,24,36,48,60]

data = {'Symbol': [], 'Momentum': []}

for symbol in global_macro:
    data['Symbol'].append(symbol)
    data['Momentum'].append(momentum.calculate_equal_weight_momentum(symbol, period))
momentum_df = pd.DataFrame(data)
momentum_df.set_index('Symbol')
momentum_df.sort_values(by='Momentum',inplace=True, ascending=False)


# ## US Sector Momentum

sector_df = pyticker.get_sector_df()
period = [1,3,6,12]
for x in list(sector_df.index):
    sector_df.loc[x,'Momentum'] = momentum.calculate_equal_weight_momentum(x, period)

sector_df.sort_values(by='Momentum', inplace=True, ascending=False)

# ## Dow Jones Equity Momentum

symbols = pyticker.get_symbols_by_index('DOW JONES')

data = {'Symbol': [], 'Momentum': []}
for symbol in symbols:
    data['Symbol'].append(symbol)
    try:
        data['Momentum'].append(momentum.calculate_equal_weight_momentum(symbol, [1,3,6,12,24,36]))
    except:
        data['Momentum'].append(0)

df = pd.DataFrame(data)
df.set_index('Symbol', inplace=True)
df = df.sort_values(by='Momentum', ascending=False)


top_three = df.head(5)

top_three_copy = top_three.copy()
for symbol in top_three.index:
    top_three_copy.loc[symbol,'Dividend_Growth'] = dividend.calcualte_avg_dividend_growth(symbol,5)
    top_three_copy.loc[symbol,'Dividend_Yield'] = dividend.calculate_current_dividend_yield(symbol)
    top_three_copy.loc[symbol,'Current_Price'] = price.get_current_price(symbol)
    top_three_copy.loc[symbol,'12M_High'] = price.calculate_prev_max_high(symbol,252)
    top_three_copy.loc[symbol,'3M_Low'] = price.calculate_prev_min_low(symbol,60)
    top_three_copy.loc[symbol,'6M_Low'] = price.calculate_prev_min_low(symbol,120)
    top_three_copy.loc[symbol,'12M_Avg'] = (price.calculate_prev_max_high(symbol,252)+price.calculate_prev_min_low(symbol,252))/2
    top_three_copy.loc[symbol,'12M_Low'] = price.calculate_prev_min_low(symbol,252)



if __name__ == '__main__':
    pass

