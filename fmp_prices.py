import pprint
import requests
import calendar
import numpy as np
import pandas as pd
import datetime as dt
from typing import List
import fmp_symbols as SYMBOLS
from credentials import FMP_API_KEY
import fmp_financials as FINANCIALS

START_DATE = dt.datetime(1970, 1, 1)
END_DATE = dt.datetime.today()

def crypto_prices(symbol: str):
    cryptos = SYMBOLS.crypto_symbols()
    if symbol in cryptos:
        data = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={FMP_API_KEY}").json()
        print(data)

def get_current_price(symbol):
    data = requests.get(f"https://financialmodelingprep.com/api/v3/quote-short/{symbol}?apikey={FMP_API_KEY}").json()
    return data[0]["price"]

def get_daily_prices(symbol):
    data = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from=1980-10-10&apikey={FMP_API_KEY}").json()
    df_data = {"Date": [], "Open": [], "High": [], "Low": [], "Close": []}

    for d in data["historical"]:
        df_data["Date"].append(d["date"])
        df_data["Open"].append(d["open"])
        df_data["High"].append(d["high"])
        df_data["Low"].append(d["low"])
        df_data["Close"].append(d["close"])

    out_df = pd.DataFrame(df_data)
    out_df = out_df[::-1]

    out_df.set_index("Date", inplace=True)

    return out_df

def get_monthly_prices(symbol: str):
    daily = pd.DataFrame()
    monthly = pd.DataFrame()

    daily[symbol] = get_daily_prices(symbol)['Close']

    for i in range(0,len(daily.index)):
        curr_date = dt.datetime.strptime(daily.index[i], "%Y-%m-%d")
        month_end_date = curr_date.replace(day = calendar.monthrange(curr_date.year, curr_date.month)[1])
        if curr_date == month_end_date:
            monthly = monthly.append(daily.loc[daily.index[i]])

    return monthly

def prev_min_low(symbol: str, period: int):
    df = get_daily_prices(symbol)
    df["Low_" + str(period)] = df["Low"].rolling(window=period).min()
    return df["Low_" + str(period)].iloc[-1]

def prev_max_high(symbol: str, period: int):
    df = get_daily_prices(symbol)
    df["High_" + str(period)] = df["High"].rolling(window=period).max()
    return df["High_" + str(period)].iloc[-1]

def calculate_return(symbol: str, period: int):
    df = get_daily_prices(symbol)
    currentPrice = df["Close"].iloc[-1]
    prevPrice = df["Close"].iloc[-period]
    ret = (currentPrice - prevPrice) / prevPrice
    return ret

def historical_monthly_momentum(symbol: str, period: int):
    monthly = get_monthly_prices(symbol)
    curr = monthly[symbol][-1]
    ret = (curr - monthly[symbol].shift(period)[-1]) / monthly[symbol].shift(period)[-1]
    return ret


if __name__ == "__main__":

    print(get_monthly_prices('AAPL'))
