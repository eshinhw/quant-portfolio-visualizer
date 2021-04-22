import json
import momentum
import pyticker
import dividend
import pandas as pd
import yfinance as yf
import datetime as dt

data_dict = {'Symbol': [], 'Dividend_Growth': [], 'Dividend_Yield': [], 'Consecutive_Yrs': []}

yrs = 15

with open('./historical_div_dow.json', 'r') as fp:
    div_dow = json.load(fp)

for symbol in list(div_dow.keys()):
    print(symbol)
    data_dict['Symbol'].append(symbol)
    # data_dict['Name'].append(yf.Ticker(symbol).info['shortName'])

    data_dict['Dividend_Growth'].append(dividend.calcualte_avg_dividend_growth(div_dow, symbol, yrs))

    data_dict['Dividend_Yield'].append(dividend.calculate_current_dividend_yield(div_dow, symbol))

    data_dict['Consecutive_Yrs'].append(div_dow[symbol][1])



