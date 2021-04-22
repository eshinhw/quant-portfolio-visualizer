import json
import pyticker
import pandas as pd
import yfinance as yf
import datetime as dt
from typing import List, Dict
import pandas_datareader.data as web
from price import calculate_current_price, calculate_historical_prices

def calculate_historical_annual_dividends(symbols: str or List[str], threshold: int) -> Dict:
    div_data = {}

    if type(symbols) == str:
        symbol_list = []
        symbol_list.append(symbols.upper())
        symbols = symbol_list

    for symbol in symbols:
        try:
            prices = yf.Ticker(symbol).history(period='max')
            dividends = prices[prices['Dividends'] > 0.001]
        except:
            continue

        if len(dividends) > 0:
            first_year = dividends.index[0].year
            last_year = dt.datetime.today().year
            annual_div = {}
            # get annual dividend sum from first year it paid out div
            for year in range(first_year, last_year):
                div_sum = dividends[dividends.index.year == year]['Dividends'].sum()
                annual_div[year] = div_sum

            if 0 in list(annual_div.values()):
                continue

            if len(annual_div) > threshold:
                div_data[symbol] = []
                div_data[symbol].append(annual_div)
                div_data[symbol].append(len(annual_div))

    return div_data

def calcualte_avg_dividend_growth(div_data: Dict, symbol: str, period: int) -> float:
    start_year = int(list(div_data[symbol][0].keys())[0])
    last_year = dt.datetime.today().year - 1
    curr_year = dt.datetime.today().year
    duration = last_year - start_year

    if period > (last_year - start_year):
        print(f"duration: {duration}")
        return 0
    try:
        prev_years = last_year - period
        rate_change = []
        for year in range(prev_years, curr_year):
            rate_change.append((div_data[symbol][0][str(year)] - div_data[symbol][0][str(year - 1)]) /
                div_data[symbol][0][str(year - 1)])
        avg_div_growth = sum(rate_change) / len(rate_change)
        # print(avg_div_growth)
        return avg_div_growth
    except:
        return 0

def calculate_current_dividend_yield(div_data: Dict, symbol: str):
    prev_year = dt.datetime.today().year - 1
    prev_annual_div = div_data[symbol][0][str(prev_year)]
    start_date = (dt.date.today() - dt.timedelta(days=5)).strftime("%Y-%m-%d")
    end_date = dt.date.today().strftime("%Y-%m-%d")

    price_data = web.DataReader(symbol, 'yahoo', start_date, end_date)
    curr_price = price_data['Adj Close'][-1]
    # curr = calculate_current_price(symbol)
    # print(curr)
    return prev_annual_div / curr_price

if __name__ == '__main__':

    div = calculate_historical_annual_dividends(['MMM'], 0)
    print(div)

    # with open('./historical_mmm.json', 'w') as fp:
    #     json.dump(div, fp)
    # with open('./historical_mmm.json', 'r') as fp:
    #     div = json.load(fp)

    # av = calcualte_avg_dividend_growth(div, 'MMM', 15)
    # # print(div)
    # print(av)

    # p = calculate_current_dividend_yield(div, 'MMM')

