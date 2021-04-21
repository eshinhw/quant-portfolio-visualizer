import json
import pyticker
import pandas as pd
import yfinance as yf
import datetime as dt
from typing import List, Dict
import pandas_datareader.data as web
from price import calculate_current_price, calculate_historical_prices

def get_historical_annual_dividends(symbol: str, threshold: int) -> Dict:
    div_data = {}
    annual_div = {}
    try:
        prices = yf.Ticker(symbol).history(period='max')
        dividends = prices[prices['Dividends'] > 0.01]
    except:
        return {}
    if len(dividends) > 0:
        first_year = dividends.index[0].year
        last_year = dt.datetime.today().year

        # get annual dividend sum from first year it paid out div
        for year in range(first_year, last_year):
            div_sum = dividends[dividends.index.year == year]['Dividends'].sum()
            annual_div[year] = div_sum

        if len(annual_div) > threshold:
            div_data[symbol] = []
            div_data[symbol].append(annual_div)
            div_data[symbol].append(len(annual_div))

    return div_data

def calcualte_avg_dividend_growth(symbol: str, period: int) -> float:
    div_data = get_historical_annual_dividends(symbol, period+1)
    start_year = list(div_data[symbol][0].keys())[0]
    last_year = dt.datetime.today().year - 1
    curr_year = dt.datetime.today().year

    if period > (last_year - start_year):
        return 0
    try:
        prev_years = last_year - period
        rate_change = []
        for year in range(prev_years, curr_year):
            rate_change.append((div_data[symbol][0][year] - div_data[symbol][0][year - 1]) /
                div_data[symbol][0][year - 1])
        avg_div_growth = sum(rate_change) / len(rate_change)
        return avg_div_growth
    except:
        return 0

def calculate_current_dividend_yield(symbol: str):

    div_data = get_historical_annual_dividends(symbol,0)
    prev_year = dt.datetime.today().year - 1
    prev_annual_div = div_data[symbol][0][prev_year]
    curr_price = calculate_current_price(symbol)
    return prev_annual_div / curr_price

def calculate_historical_avg_div_yield(symbol: str, period: int):
    start_date = (dt.date.today() - dt.timedelta(days=365*(period+1)))
    end_date = dt.date.today()
    price_data = calculate_historical_prices(symbol, start_date, end_date)

    # compute 5 years average dividend yield
    start_year = price_data.index[0].year + 1
    last_year = dt.date.today().year - 1

    dy_list = []

    div_data = get_historical_annual_dividends(symbol,period+1)

    for year in range(start_year, last_year + 1):
        yearly_data = price_data[symbol][price_data.index.year == year]
        firstPrice = yearly_data.iloc[0]
        lastPrice = yearly_data.iloc[-1]
        yearly_avg_price = (firstPrice + lastPrice) / 2
        yearly_dividend_yield = div_data[symbol][0][year] / yearly_avg_price
        dy_list.append(yearly_dividend_yield)

    historical_avg_dy = sum(dy_list) / len(dy_list)
    print(historical_avg_dy)
    return historical_avg_dy

if __name__ == '__main__':
    calculate_historical_avg_div_yield('MMM', 15)