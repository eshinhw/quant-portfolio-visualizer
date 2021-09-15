# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import fmp # fmp.py contains all helper functions working with FMP API for financial data
import pandas as pd

# # Dow Jones: select stocks which have positive 1Y, 2Y and 3Y momentum

# +
# Retrieve symbols and financials

sp500_tickers = fmp.sp500_symbols()
dow_tickers = fmp.dow_symbols()

# sp500_financials = dataSrc.financials(sp500_tickers)

df = fmp.extract_financials(dow_tickers)

# df = pd.read_csv('./R/data/dow_financials.csv')
# df = df.drop(['Unnamed: 0'], axis=1)
# df = df.dropna()

conditions = ((df["Revenue_Growth"] > 0)
              & (df["GPMargin"] > 0)
              & (df["EPS_Growth"] > 0)
              & (df["ROE"] > 0)
              & (df["DPS_Growth"] > 0)
              & (df["DivYield"] > 0))

df = df[conditions]

print(df)

# Compute historical momentum

m12_momentums = []
m24_momentums = []
m36_momentums = []
count = 0
for symbol in df["Symbol"]:
    count += 1
    m12_momentums.append(fmp.calculate_hist_momentum(symbol, 252))
    m24_momentums.append(fmp.calculate_hist_momentum(symbol, 504))
    m36_momentums.append(fmp.calculate_hist_momentum(symbol, 756))

df["m12_momentum"] = m12_momentums
df["m24_momentum"] = m24_momentums
df["m36_momentum"] = m36_momentums

positive_mom_stocks = df[(df['m12_momentum'] > 0) & (df['m24_momentum'] > 0)
                         & (df['m36_momentum'] > 0)]
positive_mom_stocks
# -

# # Calculate stocks' discount rate from 52W high

# +
watchlist = positive_mom_stocks[["symbol", "name"]].copy()

# Update current prices, 52W High and Discount %

currentPrices = []
highs = []
discounts = []
count = 0

for symbol in watchlist["symbol"]:
    count += 1
    print(f"{symbol}: {count}/{len(watchlist['symbol'])}")
    currentPrice = fmp.get_current_price(symbol)
    high = fmp.calculate_prev_max_high(symbol, 252)
    discount_pct = (currentPrice - high) / high * 100

    currentPrices.append(currentPrice)
    highs.append(high)
    discounts.append(discount_pct)

watchlist["Current Price"] = currentPrices
watchlist["52W_High"] = highs
watchlist["Discount (%)"] = discounts

watchlist = watchlist.sort_values(by="Discount (%)")
watchlist
# -

# # Consider buying if discounted more than 15%

buylist = watchlist[watchlist['Discount (%)'] < -15]
buylist

# # S&P500

# +
# Retrieve symbols and financials

sp500_tickers = fmp.sp500_symbols()

df = fmp.extract_financials(sp500_tickers)

# df = pd.read_csv('./R/data/dow_financials.csv')
# df = df.drop(['Unnamed: 0'], axis=1)
# df = df.dropna()

conditions = ((df["Revenue_Growth"] > 0)
              & (df["GPMargin"] > 0)
              & (df["EPS_Growth"] > 0)
              & (df["ROE"] > 0)
              & (df["DPS_Growth"] > 0)
              & (df["DivYield"] > 0))

df = df[conditions]

# Compute historical momentum

m12_momentums = []
m24_momentums = []
m36_momentums = []
count = 0
for symbol in df["symbol"]:
    count += 1
    m12_momentums.append(fmp.calculate_hist_momentum(symbol, 252))
    m24_momentums.append(fmp.calculate_hist_momentum(symbol, 504))
    m36_momentums.append(fmp.calculate_hist_momentum(symbol, 756))

df["m12_momentum"] = m12_momentums
df["m24_momentum"] = m24_momentums
df["m36_momentum"] = m36_momentums

positive_mom_stocks = df[(df['m12_momentum'] > 0) & (df['m24_momentum'] > 0)
                         & (df['m36_momentum'] > 0)]
positive_mom_stocks

# +
watchlist = positive_mom_stocks[["symbol", "name"]].copy()

# Update current prices, 52W High and Discount %

currentPrices = []
highs = []
discounts = []
count = 0

for symbol in watchlist["symbol"]:
    count += 1
    print(f"{symbol}: {count}/{len(watchlist['symbol'])}")
    currentPrice = fmp.get_current_price(symbol)
    high = fmp.calculate_prev_max_high(symbol, 252)
    discount_pct = (currentPrice - high) / high * 100

    currentPrices.append(currentPrice)
    highs.append(high)
    discounts.append(discount_pct)

watchlist["Current Price"] = currentPrices
watchlist["52W_High"] = highs
watchlist["Discount (%)"] = discounts

watchlist = watchlist.sort_values(by="Discount (%)")
watchlist
# -

buylist = watchlist[watchlist['Discount (%)'] < -15]
buylist







# +
# #!jupyter nbconvert --to script --no-prompt analysis.ipynb
