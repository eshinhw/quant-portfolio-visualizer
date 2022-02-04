import pprint
import requests
import calendar
import numpy as np
import pandas as pd
import datetime as dt
from typing import List
from credentials import FMP_API_KEY

START_DATE = dt.datetime(1970, 1, 1)
END_DATE = dt.datetime.today()


def retrieve_financials(symbols):

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
            profile = requests.get(f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FMP_API_KEY}").json()[0]
            ratio_ttm = requests.get(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={FMP_API_KEY}").json()[0]
            growth = requests.get(f"https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?period=quarter&limit=20&apikey={FMP_API_KEY}").json()[0]
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
