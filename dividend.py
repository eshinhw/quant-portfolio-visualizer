import json
import pandas as pd
import yfinance as yf
import datetime as dt
from typing import List, Dict
import pandas_datareader.data as web

def get_historical_annual_dividends(symbol: str) -> Dict:
    div_data = {}
    annual_div = {}
    prices = yf.Ticker(symbol).history(period='max')
    dividends = prices[prices['Dividends'] > 0]
    if len(dividends) > 0:
        first_year = dividends.index[0].year
        last_year = dt.datetime.today().year

        # get annual dividend sum from first year it paid out div
        for year in range(first_year, last_year):
            div_sum = dividends[dividends.index.year == year]['Dividends'].sum()
            annual_div[year] = div_sum

        div_data[symbol] = []
        div_data[symbol].append(annual_div)
        div_data[symbol].append(len(annual_div))

    return div_data

def get_consecutive_dividend_payout_history(symbol: str, threshold: int) -> bool:
    div_data = get_historical_annual_dividends(symbol)
    years = div_data[symbol][1]
    if years >= threshold:
        return True
    return False

def calcualte_avg_dividend_growth(symbol: str, period: int):
    div_data = get_historical_annual_dividends(symbol)
    start_year = list(div_data[symbol][0].keys())[0]
    last_year = dt.datetime.today().year - 1
    curr_year = dt.datetime.today().year
    duration = last_year - start_year

    if period > duration:
        return None

    prev_years = last_year - period
    rate_change = []
    for year in range(prev_years, curr_year):
        rate_change.append(100 * (div_data[symbol][0][year] - div_data[symbol][0][year - 1]) /
            div_data[symbol][0][year - 1])
    avg_div_growth = sum(rate_change) / len(rate_change)
    return avg_div_growth

if __name__ == '__main__':
    print(get_historical_annual_dividends('MMM'))
    print(calcualte_avg_dividend_growth('MMM', 80))
    #print(get_num_dividend_payout_history(['MMM'], 30))