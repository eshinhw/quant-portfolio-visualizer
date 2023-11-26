import datetime as dt
import numpy as np
import yfinance as yf

import pandas as pd


class BasePortfolio:
    def __init__(self, name: str, assets: list[str], weights: list[float]) -> None:
        self.name = name
        self.assets = assets
        self.weights = weights

    def __str__(self) -> str:
        return self.name

    def monthly_prices(self):
        prices = yf.download(self.assets, interval="1mo", progress=False)
        prices = prices.loc[:, "Adj Close"]
        prices.columns = self.assets
        return prices

    def monthly_returns(self):
        # monthly returns calculation
        prices = self.monthly_prices()
        monthly_returns = prices.pct_change().dropna()
        return monthly_returns

    def port_cum_returns(self):
        # portfolio cumulative returns
        monthly_returns = self.monthly_returns()
        monthly_returns = monthly_returns.shift(-1)
        monthly_returns["port"] = monthly_returns.dot(self.weights)
        cum_returns = np.exp(np.log1p(monthly_returns["port"]).cumsum())[:-1]
        return cum_returns

    def cagr(self):
        port_cum_returns = self.port_cum_returns()
        first_value = port_cum_returns[0]
        last_value = port_cum_returns[-1]
        years = len(port_cum_returns.index) / 12
        cagr = (last_value / first_value) ** (1 / years) - 1
        return round(cagr, 3)

    def mdd(self):
        drawdown = self.drawdown()
        port_mdd = drawdown.min()
        return round(port_mdd, 3)

    def drawdown(self):
        port_cum_returns = self.port_cum_returns()
        previous_peaks = port_cum_returns.cummax()
        drawdown = (port_cum_returns - previous_peaks) / previous_peaks
        return drawdown


if __name__ == "__main__":
    pass
