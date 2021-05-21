import os
import json
import secret
import requests
import pandas as pd
import datetime as dt
from typing import List, Dict
import pandas_datareader.data as web
from pytickersymbols import PyTickerSymbols

START_DATE = dt.datetime(1970, 1, 1)
END_DATE = dt.datetime.today()
MOMENTUM_PERIODS = [12, 36, 60]
FMP_API = secret.FMP_API_KEYS


"""
I can do lots of quantamental analysis using financial modeling prep API which I will subscribe.
GET list of S&P 500 symbols (Pyticker)
"""


def get_sp500_symbols(index: str) -> Dict:
    data = {}
    pyticker = PyTickerSymbols()
    try:
        sp500 = list(pyticker.get_stocks_by_index(index))
    except:
        print("index not valid")
        return

    for record in sp500:
        symbol = record["symbol"]
        try:
            sector = record["industries"][0]
        except:
            sector = "N/A"
        name = record["name"]
        data[symbol] = {}
        data[symbol]["name"] = name
        data[symbol]["sector"] = sector

    return data


"""
CALCULATE historical momentum (yahoo finance)
1. calculate historical monthly prices for each stock
2. momentum: Average of previous months in MOMENTUM_PERIODS

Statistical Distribution for reasonable thresholds
"""


def get_daily_prices(symbol, start_date=None, end_date=None):
    return web.DataReader(symbol, "yahoo", start_date, end_date)


def get_historical_monthly_prices(symbol: str, start_date, end_date):
    prices = get_daily_prices(symbol, start_date, end_date)
    prices.dropna(inplace=True)
    prices.reset_index(inplace=True)
    prices = prices[["Date", "Adj Close"]]
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


def calculate_equal_weight_momentum(
    symbol: str, periods: List[int], start_date, end_date
):
    ret = []
    monthly_prices = get_historical_monthly_prices(symbol, start_date, end_date)
    for period in periods:
        monthly_returns = monthly_prices.apply(lambda x: x / x.shift(period) - 1, axis=0)
        monthly_returns = monthly_returns.rename(columns={"Adj Close": "Returns"})
        ret.append(monthly_returns["Returns"].iloc[-1])
    return sum(ret) / len(ret)


"""
GET dividend data (financialmodelingprep API)
1. Current Dividend Yield
2. Dividend Grwoth: Average (3, 5)
3. Dividend Payout
"""


def dividend_paying_stocks():

    div_paying_stocks = []
    sp500 = requests.get(f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={FMP_API}").json()

    count = 0
    for stock in sp500:
        count += 1
        print(f"{count}/{len(sp500)}")
        symbol = stock["symbol"]
        ratios = requests.get(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={FMP_API}").json()[0]
        div_yield = ratios["dividendYieldTTM"]

        if div_yield:
            print(f"{symbol} ADDED!")
            div_paying_stocks.append(symbol)

    with open("./div_stocks_sp500.json", "w") as fp:
        json.dump(div_paying_stocks, fp)

def dividend_growth(symbols: List[str]):
    growth = requests.get(f"https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?limit=20&apikey={FMP_API}").json()[0]
    div_growth = growth['fiveYDividendperShareGrowthPerShare']

def high_momentum(symbols: List[str]):
    pass

def profitability(symbols: List[str]):
    pass


def fmp_datareader():

    sp500 = requests.get(
        f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={FMP_API}"
    ).json()
    data = {
        "Symbol": [],
        "Market_Cap": [],
        "ROE": [],
        "FiveY_Revenue_Growth": [],
        "FiveY_NetIncome_Growth": [],
        "FiveY_Div_Per_Share_Growth": [],
    }
    count = 0
    for stock in sp500:
        count += 1
        print(f"{count}/{len(sp500)}")
        symbol = stock["symbol"]
        print(symbol)
        growth = requests.get(
            f"https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?limit=20&apikey={FMP_API}"
        ).json()[0]
        div_growth = growth["fiveYDividendperShareGrowthPerShare"]
        # print(div_growth)

        mom = calculate_equal_weight_momentum(
            symbol, MOMENTUM_PERIODS, START_DATE, END_DATE
        )
        # print(mom)

        if div_growth > 0.1 and mom > 1:

            print(f"{symbol} SELECTED!")

            ratios = requests.get(
                f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={FMP_API}"
            ).json()[0]
            market_cap = requests.get(
                f"https://financialmodelingprep.com/api/v3/market-capitalization/{symbol.upper()}?apikey={FMP_API}"
            ).json()[0]["marketCap"]

            data["Symbol"].append(symbol)
            data["Market_Cap"].append(market_cap)
            data["ROE"].append(ratios["returnOnEquityTTM"])
            data["FiveY_Revenue_Growth"].append(growth["fiveYRevenueGrowthPerShare"])
            data["FiveY_NetIncome_Growth"].append(
                growth["fiveYNetIncomeGrowthPerShare"]
            )
            data["FiveY_Div_Per_Share_Growth"].append(
                growth["fiveYDividendperShareGrowthPerShare"]
            )

    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":

    # df = fmp_datareader()
    # print(df)

    #dividend_paying_stocks()
    with open('./div_stocks_sp500.json', 'r') as fp:
        data = json.load(fp)
    print(data)
    print()
    # print(calculate_equal_weight_momentum('MMM', MOMENTUM_PERIODS, START_DATE, END_DATE))

    # # If you already have json file saved on local dir, execute remaining codes for momentum and dividend
    # if os.path.exists("./sp500_data.json"):
    #     fp = open("./sp500_data.json", "r")
    #     sp500 = json.load(fp)

    #     high_momentum = []

    #     for symbol in sp500.keys():
    #         mom = sp500[symbol]["momentum"]
    #         if mom > 2:
    #             high_momentum.append(symbol)

    #     df = fmp_datareader(high_momentum)
    #     print(df)

    # # If you don't have json file on your local dir,
    # # get symbol data first and save it as sp500_data.json on the same dir
    # else:
    #     # sp500 = get_sp500_symbols("S&P 500")
    #     # sp500_symbols = list(sp500.keys())
    #     # count = 0
    #     # for symbol in sp500_symbols:
    #     #     count += 1
    #     #     print(f"{count}/{len(sp500_symbols)}")
    #     #     try:
    #     #         sp500[symbol]["momentum"] = calculate_equal_weight_momentum(
    #     #             symbol, MOMENTUM_PERIODS, START_DATE, END_DATE
    #     #         )
    #     #     except KeyError as e:
    #     #         print(f"{symbol}: ({type(e).__name__}) {e}")
    #     #         sp500[symbol]["momentum"] = -1
    #     #         continue
    #     #     except Exception as e:
    #     #         print(f"{symbol}: ({type(e).__name__}) {e}")
    #     #         sp500[symbol]["momentum"] = -1
    #     #         continue
