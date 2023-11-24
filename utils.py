import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf


def monthly_prices(assets):
    monthly_prices = pd.DataFrame()
    for asset in assets:
        monthly_prices[asset] = yf.download(
            asset, start=dt.datetime(2018, 1, 1), end=dt.datetime.today(), interval="1mo", progress=False
        )["Adj Close"]
    monthly_prices.dropna(inplace=True)
    return monthly_prices


def monthly_returns(assets):
    monthly_returns = monthly_prices(assets).pct_change()
    monthly_returns.dropna(inplace=True)
    return monthly_returns


# def cumulative_return(assets):
#     # we have to shift the returns upward by one to align with momentum signal above.
#     monthly_returns = monthly_returns(assets)
#     monthly_returns = monthly_returns[self.mom_rank.index[0]:].shift(-1)
#     vaa_port_returns = np.multiply(
#         self.mom_rank, monthly_returns).sum(axis=1)
#     vaa_port_cum_returns = np.exp(np.log1p(vaa_port_returns).cumsum())[:-1]
#     return vaa_port_cum_returns


# def cagr(self):
#     first_value = self.port_cum_returns[0]
#     last_value = self.port_cum_returns[-1]
#     years = len(self.port_cum_returns.index)/12
#     cagr = (last_value/first_value)**(1/years) - 1
#     return cagr


# def mdd(self):
#     previous_peaks = self.port_cum_returns.cummax()
#     drawdown = (self.port_cum_returns - previous_peaks) / previous_peaks
#     port_mdd = drawdown.min()
#     return port_mdd


if __name__ == "__main__":
    print(monthly_prices(["AAPL"]))
    print(monthly_returns(["aapl"]))
