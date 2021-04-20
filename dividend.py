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

def calcualte_avg_dividend_growth(symbol: str, period: int) -> float:
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

def calculate_current_dividend_yield(symbol: str):

    div_data = get_historical_annual_dividends(symbol)

    start_date = (dt.date.today() - dt.timedelta(days=5)).strftime("%Y-%m-%d")
    end_date = dt.date.today().strftime("%Y-%m-%d")

    price_data = web.DataReader(symbol, 'yahoo', start_date, end_date)

    prev_year = dt.datetime.today().year - 1

    prev_annual_div = div_data[symbol][0][prev_year]

    return prev_annual_div / price_data['Adj Close'][-1]

def _get_close_and_historical_div_yield(symbol, period):
    startDate = (dt.date.today() - dt.timedelta(days=(365*(period + 1)))
                 ).strftime("%Y-%m-%d")
    endDate = dt.date.today().strftime("%Y-%m-%d")
    price_data = web.DataReader(symbol, 'yahoo', startDate,
                                endDate)

    # compute 5 years average dividend yield
    start_year = price_data.index[0].year + 1
    last_year = dt.date.today().year - 1

    dy_list = []

    for year in range(start_year, last_year + 1):
        yearly_data = price_data['Close'][price_data.index.year == year]
        firstPrice = yearly_data.iloc[0]
        lastPrice = yearly_data.iloc[-1]
        yearly_avg_price = (firstPrice + lastPrice) / 2
        yearly_dividend_yield = div_data[symbol.upper()][0][year] / yearly_avg_price
        dy_list.append(yearly_dividend_yield)

    historical_avg_dy = round((sum(dy_list) / len(dy_list)) * 100, 2)
    # print(historical_avg_dy)

    close = price_data['Adj Close'].iloc[-1].round(2)
    # print(close)
    #return (close, historical_avg_dy)
    return historical_avg_dy

if __name__ == '__main__':
    print(get_historical_annual_dividends('MMM'))
    print(calcualte_avg_dividend_growth('MMM', 80))
    print(calculate_current_dividend_yield('MMM'))
    #print(get_num_dividend_payout_history(['MMM'], 30))