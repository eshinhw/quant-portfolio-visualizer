import json
import requests
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
from typing import List
from mydb import db_master
import pandas_datareader.data as web


def get_historical_daily_prices(symbol: str, start_date=None, end_date=None):
    db = db_master(symbol)
    try:
        return db.download_price_history_to_df()
    except:
        db.upload_price_history_to_sql()
        return db.download_price_history_to_df()

def get_current_price(symbol: str) -> float:
    prices = get_historical_daily_prices(symbol)
    return prices['Adj_Close'][-1]

def get_historical_monthly_prices(symbol: str, start_date=None, end_date=None):
    prices = get_historical_daily_prices(symbol, start_date, end_date)
    prices.dropna(inplace=True)
    prices.reset_index(inplace=True)
    prices = prices[['Date', 'Adj_Close']]
    prices['STD_YM'] = prices['Date'].map(lambda x : dt.datetime.strftime(x, '%Y-%m'))
    month_list = prices['STD_YM'].unique()
    monthly_prices = pd.DataFrame()
    for m in month_list:
        monthly_prices = monthly_prices.append(prices[prices['STD_YM'] == m].iloc[-1,:])
    monthly_prices = monthly_prices.drop(columns=['STD_YM'], axis=1)
    monthly_prices.set_index('Date', inplace=True)
    return monthly_prices[:-1]

def calculate_prev_min_low(symbol: str, period: int):
    df = get_historical_daily_prices(symbol)
    df["Low_" + str(period)] = df["Low"].shift(1).rolling(window=period).min()

    return df["Low_" + str(period)].iloc[-1]


def calculate_prev_max_high(symbol: str, period: int):
    df = get_historical_daily_prices(symbol)
    print(df)
    df["High_" + str(period)] = df["High"].shift(1).rolling(window=period).max()
    return df["High_" + str(period)].iloc[-1]



# def calculate_periodic_returns(symbol, period):
#     monthly_prices = get_historical_monthly_prices(symbol)
#     ret = []
#     for p in period:
#         monthly_returns = monthly_prices.apply(lambda x: x/x.shift(period) - 1, axis=0)
#         monthly_returns = monthly_returns.rename(columns={'Adj_Close': 'Returns'})
#         ret.append(monthly_returns['Returns'].iloc[-1])
#     return monthly_returns

# def get_price_and_return_data(symbol, start_date, end_date):

#     start = dt.datetime.strptime(start_date, '%Y-%m-%d')
#     end = dt.datetime.strptime(end_date, '%Y-%m-%d')

#     df = pd.DataFrame()

#     df[symbol] = web.DataReader(symbol, 'yahoo', start, end)['Adj Close']
#     df["daily_returns"] = df.pct_change()
#     df["cumulative_returns"] = (1+df["daily_returns"]).cumprod()
#     df["cumulative_returns"].dropna(inplace=True)
#     return df

# def calculate_cagr(df):

#     return df.iloc[-1,2] ** (252/len(df.index)) - 1

# def calculate_mdd(df):
#     historical_max = df.iloc[:,0].cummax()
#     daily_drawdown = df.iloc[:,0] / historical_max - 1
#     historical_dd = daily_drawdown.cummin()
#     #print(type(historical_dd))
#     return historical_dd.min()

# def calculate_vol(df):
#     return np.std(df.iloc[:,1]) * np.sqrt(252)

# def calculate_ex_post_sharpe(df):
#     return np.mean(df.iloc[:,1]) / np.std(df.iloc[:,1]) * np.sqrt(252)

if __name__ == '__main__':
    x = calculate_prev_max_high('aapl', 365)
    print(x)
