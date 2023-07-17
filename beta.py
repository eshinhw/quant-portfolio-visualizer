import yfinance as yf
import pandas as pd
import statsmodels.api as sm

tickers = ["SPY", "JPM"]

all_data = {}

for ticker in tickers:
    all_data[ticker] = yf.download(ticker, start="2020-01-01", end="2021-12-31")

prices = pd.DataFrame({tic: data["Close"] for tic, data in all_data.items()})
ret = prices.pct_change().dropna()
print(prices)
print(ret)

ret["intercept"] = 1
reg = sm.OLS(ret[["JPM"]], ret[["SPY", "intercept"]]).fit()
reg.summary()
print(reg.summary())
print(reg.params.iloc[0])
