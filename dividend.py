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
        div = db.dividend_history_import_to_df()
    except:
        db.dividend_history_export_to_sql()
        div = db.dividend_history_import_to_df()
    return div

def calcualte_avg_dividend_growth(symbol: str, period=None) -> float:
    annual_div = get_historical_annual_dividends(symbol)
    changes = annual_div.pct_change()

    if period:
        changes = changes.tail(period)
        return changes['Dividends'].mean()
    else:
        return changes['Dividends'].mean()


def calculate_current_dividend_yield(symbol: str):
    div = get_historical_annual_dividends(symbol)
    latest_div = div['Dividends'][-1]
    curr_price = get_current_price(symbol)
    return latest_div/curr_price

if __name__ == '__main__':
    ch = calcualte_avg_dividend_growth('MMM',10)
    print(ch)


