import datetime as dt
import smtplib
from email.message import EmailMessage
from typing import List

import numpy as np
import pandas as pd
import requests

import credentials

FMP_API_KEY = credentials.FMP_API_KEYS
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
        "symbol": [],
        "name": [],
        "exchange": [],
        "sector": [],
        "industry": [],
        "marketCap(B)": [],
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

        financials_data["symbol"].append(symbol)

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

        financials_data["name"].append(profile["companyName"])
        financials_data["exchange"].append(profile["exchangeShortName"])
        financials_data["sector"].append(profile["sector"])
        financials_data["industry"].append(profile["industry"])
        financials_data["marketCap(B)"].append(profile["mktCap"] / 1000000000)
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
        f"https://financialmodelingprep.com/api/v3/quote-short/{symbol}?apikey={credentials.FMP_API_KEYS}"
    ).json()
    return data[0]["price"]

def get_daily_prices(symbol):
    data = requests.get(
        f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={credentials.FMP_API_KEYS}"
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

def get_historical_monthly_prices(symbol: str):
    prices = get_daily_prices(symbol)
    prices.dropna(inplace=True)
    prices.reset_index(inplace=True)
    prices = prices[["Date", "Close"]]
    prices["STD_YM"] = prices["Date"].map(lambda x: dt.datetime.strftime(x, "%Y-%m"))
    month_list = prices["STD_YM"].unique()
    monthly_prices = pd.DataFrame()
    for m in month_list:
        monthly_prices = monthly_prices.append(
            prices[prices["STD_YM"] == m].iloc[-1, :]
        )
    monthly_prices = monthly_prices.drop(columns=["STD_YM"], axis=1)
    monthly_prices.set_index("Date", inplace=True)
    return monthly_prices[:-1]


def calculate_momentum(symbol: str, periods: List[int]):
    ret = []
    ret.append(symbol)
    monthly_prices = get_historical_monthly_prices(symbol)
    for period in periods:
        monthly_returns = monthly_prices.apply(
            lambda x: x / x.shift(period) - 1, axis=0
        )
        monthly_returns = monthly_returns.rename(columns={"Adj Close": "Returns"})
        mom = float(monthly_returns["Returns"][-1])
        if mom == np.nan:
            mom = float("-inf")
        ret.append(mom)
    return ret


def sendEmail(subject, curr_pos, filters, watchlist):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = credentials.GMAIL_ADDRESS
    msg["To"] = credentials.GMAIL_ADDRESS
    # msg.set_content("hello?")

    msg.add_alternative(
        f"""\

        <!DOCTYPE html>
        <html>
            <body>
                <p> Hello Investors,<br> Below is the daily summary of your portfolio and updated stock watchlist.<br> Have a good evening :) </p>
                <h1> Portfolio Overview </h1>
                <h3> Investment Summary </h3>
                {curr_pos}
                <h1> Watchlist - S&P500 Discounted Stocks </h1>
                <h3> Conditional Filters </h3>
                {filters}
                <br>
                {watchlist}
            </body>
        </html>
    """,
        subtype="html",
    )
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(credentials.GMAIL_ADDRESS, credentials.GMAIL_PW)
        smtp.send_message(msg)


if __name__ == "__main__":

    sp500 = sp500_symbols()
    dow = dow_symbols()
    extract_financials(dow)
