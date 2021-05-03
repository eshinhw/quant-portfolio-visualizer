import json
import pyticker
import pandas as pd
import yfinance as yf
import datetime as dt
from mydb import db_master
from typing import List, Dict
from price import get_current_price
import pandas_datareader.data as web

def get_historical_annual_dividends(symbol):
    db = db_master(symbol)
    try:
        div = db.download_dividend_history_to_df()
    except:
        db.upload_dividend_history_to_sql()
        div = db.download_dividend_history_to_df()
    return div

def calcualte_avg_dividend_growth(symbol: str, period=None) -> float:
    annual_div = get_historical_annual_dividends(symbol)
    changes = annual_div.pct_change()

    if period:
        changes = changes.tail(period)
        if changes['Dividends'].mean() == float('inf'):
            return np.nan
        else:
            return changes['Dividends'].mean()
    else:
        if changes['Dividends'].mean() == float('inf'):
            return np.nan
        else:
            return changes['Dividends'].mean()



def calculate_current_dividend_yield(symbol: str):
    div = get_historical_annual_dividends(symbol)
    latest_div = div['Dividends'].iloc[-1]
    curr_price = get_current_price(symbol)
    return latest_div/curr_price

def exists_dividends(symbol: str):
    data = yf.Ticker(symbol).history(period='max')
    div = data[data['Dividends'] > 0.01]
    # print(div)
    # print(not div.empty)
    # print(not 0 in div['Dividends'].values)
    return (not div.empty) and (not 0 in div['Dividends'].values)

if __name__ == '__main__':
    pass