import datetime as dt

from typing import List

import numpy as np
import pandas as pd
import requests
import pprint

import src.credentials as cred

FMP_API_KEY = cred.FMP_API_KEYS
START_DATE = dt.datetime(1970, 1, 1)
END_DATE = dt.datetime.today()


def sp500_symbols():
    symbols = []
    sp500 = requests.get(
        f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={FMP_API_KEY}"
    ).json()

    for data in sp500:
        symbols.append(data["symbol"])

    return symbols


def dow_symbols():
    symbols = []
    dow = requests.get(
        f"https://financialmodelingprep.com/api/v3/dowjones_constituent?apikey={FMP_API_KEY}"
    ).json()

    for data in dow:
        symbols.append(data["symbol"])

    return symbols


def extract_financials(symbols):

    if len(symbols) < 50:
        fname = "dow"
    elif len(symbols) < 300:
        fname = "nasdaq"
    else:
        fname = "sp500"

    financials_data = {
        "Symbol": [],
        "Name": [],
        "Exchange": [],
        "Sector": [],
        "Industry": [],
        "MarketCap(B)": [],
        "Revenue_Growth": [],
        "ROE": [],
        "GPMargin": [],
        "EPS_Growth": [],
        "DivYield": [],
        "DPS": [],
        "DPS_Growth": [],
    }

    count = 0
    for symbol in symbols:
        count += 1
        print(f"{symbol}: {count}/{len(symbols)}")

        financials_data["Symbol"].append(symbol)

        try:
            profile = requests.get(
                f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FMP_API_KEY}"
            ).json()[0]
            ratio_ttm = requests.get(
                f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={FMP_API_KEY}"
            ).json()[0]
            growth = requests.get(
                f"https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?period=quarter&limit=20&apikey={FMP_API_KEY}"
            ).json()[0]
        except:
            continue

        financials_data["Name"].append(profile["companyName"])
        financials_data["Exchange"].append(profile["exchangeShortName"])
        financials_data["Sector"].append(profile["sector"])
        financials_data["Industry"].append(profile["industry"])
        financials_data["MarketCap(B)"].append(profile["mktCap"] / 1000000000)
        financials_data["DivYield"].append(ratio_ttm["dividendYieldTTM"])
        financials_data["DPS"].append(ratio_ttm["dividendPerShareTTM"])
        financials_data["DPS_Growth"].append(
            growth["fiveYDividendperShareGrowthPerShare"]
        )
        financials_data["ROE"].append(ratio_ttm["returnOnEquityTTM"])
        financials_data["GPMargin"].append(ratio_ttm["grossProfitMarginTTM"])
        financials_data["EPS_Growth"].append(growth["epsgrowth"])
        financials_data["Revenue_Growth"].append(growth["fiveYRevenueGrowthPerShare"])

    df_financials = pd.DataFrame(financials_data)

    # df_financials.to_csv(f'./R/data/{fname}_financials.csv')

    return df_financials


def get_current_price(symbol):

    data = requests.get(
        f"https://financialmodelingprep.com/api/v3/quote-short/{symbol}?apikey={FMP_API_KEY}"
    ).json()
    return data[0]["price"]

def get_daily_prices(symbol):
    data = requests.get(
        f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={FMP_API_KEY}"
    ).json()
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


def calculate_prev_min_low(symbol: str, period: int):
    df = get_daily_prices(symbol)
    df["Low_" + str(period)] = df["Low"].rolling(window=period).min()
    return df["Low_" + str(period)].iloc[-1]


def calculate_prev_max_high(symbol: str, period: int):
    df = get_daily_prices(symbol)
    df["High_" + str(period)] = df["High"].rolling(window=period).max()
    return df["High_" + str(period)].iloc[-1]

def calculate_hist_momentum(symbol: str, period: int):
    df = get_daily_prices(symbol)
    currentPrice = df["Close"].iloc[-1]
    prevPrice = df["Close"].iloc[-period]
    ret = (currentPrice - prevPrice) / prevPrice
    return ret

def get_monthly_prices(symbol: str):
    daily = pd.DataFrame()
    monthly = pd.DataFrame()

    daily[symbol] = get_daily_prices(symbol)['Close']

    for i in range(0,len(daily.index)-1):
        currMonth = dt.datetime.strptime(daily.index[i], '%Y-%m-%d').month
        nextMonth = dt.datetime.strptime(daily.index[i+1], '%Y-%m-%d').month

        if currMonth != nextMonth:
            monthly = monthly.append(daily.loc[daily.index[i]])

    return monthly



def calculate_momentum(symbol: str, period: int):
    monthly = get_monthly_prices(symbol)
    curr = monthly[symbol][-1]
    ret = (curr - monthly[symbol].shift(period)[-1]) / monthly[symbol].shift(period)[-1]
    return ret





if __name__ == "__main__":

    sp500_symbols()
