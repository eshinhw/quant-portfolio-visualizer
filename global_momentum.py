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


