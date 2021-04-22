import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
from typing import List
import pandas_datareader.data as web



def calculate_current_price(symbol: str) -> float:
    start_date = (dt.date.today() - dt.timedelta(days=5)).strftime("%Y-%m-%d")
    end_date = dt.date.today().strftime("%Y-%m-%d")

    price_data = web.DataReader(symbol, 'yahoo', start_date, end_date)
    return price_data['Adj Close'][-1]

def calculate_historical_prices(symbols: str or List[str], start_date: dt, end_date: dt):
    prices = pd.DataFrame()
    if type(symbols) == str:
        prices[symbols] = web.DataReader(symbols, 'yahoo', start_date, end_date)['Adj Close']
    if type(symbols) == list:
        for symbol in symbols:
            prices[symbol] = web.DataReader(symbol, 'yahoo', start_date, end_date)['Adj Close']
    return prices

def convert_monthly_prices(symbols: str or List[str], start_date: dt, end_date: dt):
    prices = calculate_historical_prices(symbols, start_date, end_date)
    prices.dropna(inplace=True)
    prices.reset_index(inplace=True)
    prices['STD_YM'] = prices['Date'].map(lambda x : dt.datetime.strftime(x, '%Y-%m'))
    month_list = prices['STD_YM'].unique()
    monthly_prices = pd.DataFrame()
    for m in month_list:
        monthly_prices = monthly_prices.append(prices[prices['STD_YM'] == m].iloc[-1,:])
    monthly_prices = monthly_prices.drop(columns=['STD_YM'], axis=1)
    monthly_prices.set_index('Date', inplace=True)
    return monthly_prices

def calculate_periodic_returns(monthly_prices, period):
    monthly_copy = monthly_prices.copy()
    monthly_copy = monthly_copy.apply(lambda x: x.shift(1)/x.shift(period+1) - 1, axis=0)
    monthly_copy.dropna(inplace=True)
    return monthly_copy

def get_price_and_return_data(symbol, start_date, end_date):

    start = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end = dt.datetime.strptime(end_date, '%Y-%m-%d')

    df = pd.DataFrame()

    df[symbol] = web.DataReader(symbol, 'yahoo', start, end)['Adj Close']
    df["daily_returns"] = df.pct_change()
    df["cumulative_returns"] = (1+df["daily_returns"]).cumprod()
    df["cumulative_returns"].dropna(inplace=True)
    return df

def calculate_cagr(df):

    return df.iloc[-1,2] ** (252/len(df.index)) - 1

def calculate_mdd(df):
    historical_max = df.iloc[:,0].cummax()
    daily_drawdown = df.iloc[:,0] / historical_max - 1
    historical_dd = daily_drawdown.cummin()
    #print(type(historical_dd))
    return historical_dd.min()

def calculate_vol(df):

    return np.std(df.iloc[:,1]) * np.sqrt(252)

def calculate_ex_post_sharpe(df):
    return np.mean(df.iloc[:,1]) / np.std(df.iloc[:,1]) * np.sqrt(252)

if __name__ == '__main__':
    print(calculate_current_price('TRV'))