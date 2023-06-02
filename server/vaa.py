"""
Vigilant Asset Allocation (VAA) Implementation Source Codes
"""

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf


class VAA():

    def __init__(self) -> None:
        self.offensive_assets = ['SPY', 'VEA', 'VWO', 'AGG']
        self.defensive_assets = ['SHY', 'IEF', 'LQD']
        self.prices = self.monthly_prices()
        self.mom_score = self.momentum_score()
        self.mom_rank = self.momentum_score_rank()
        self.port_cum_returns = self.cumulative_return()

    def __str__(self) -> str:
        return "VAA"

    def _weighted_momentum_score(self, x):
        """
        momentum_periods = [1,3,6,12]
        momentum_weights = np.array([12,4,2,1])
        """
        m1 = x / x.shift(1) - 1
        m3 = x / x.shift(3) - 1
        m6 = x / x.shift(6) - 1
        m12 = x / x.shift(12) - 1
        return 12 * m1 + 4 * m3 + 2 * m6 + 1 * m12

    def monthly_prices(self):
        vaa_assets = self.offensive_assets + self.defensive_assets
        monthly_prices = pd.DataFrame()
        for asset in vaa_assets:
            monthly_prices[asset] = yf.download(asset, start=dt.datetime(
                2018, 1, 1), end=dt.datetime.today(), interval='1mo', progress=False)['Adj Close']
        monthly_prices.dropna(inplace=True)
        return monthly_prices

    def momentum_score(self):
        # calcuate weighted momentum scores at each month
        mom_score = self.prices.copy().apply(self._weighted_momentum_score, axis=0)
        mom_score.dropna(inplace=True)
        return mom_score

    def momentum_score_rank(self):
        # print(self.mom_score[self.offensive_assets])
        # print(self.mom_score[self.defensive_assets])
        for date in self.mom_score.index:
            if (self.mom_score.loc[date, self.offensive_assets] < 0).any():
                # check defensive assets
                self.mom_score.loc[date, 'SPY'] = float("-inf")
                self.mom_score.loc[date, 'VEA'] = float("-inf")
                self.mom_score.loc[date, 'VWO'] = float("-inf")
                self.mom_score.loc[date, 'AGG'] = float("-inf")

                if (self.mom_score.loc[date, self.defensive_assets] < 0).all():
                    # hold cash
                    self.mom_score.loc[date, 'SHY'] = float("-inf")
                    self.mom_score.loc[date, 'IEF'] = float("-inf")
                    self.mom_score.loc[date, 'LQD'] = float("-inf")

            else:
                # invest offensive asset
                self.mom_score.loc[date, 'SHY'] = float("-inf")
                self.mom_score.loc[date, 'IEF'] = float("-inf")
                self.mom_score.loc[date, 'LQD'] = float("-inf")

        # rank across columns
        momentum_rank = self.mom_score.rank(axis=1, ascending=False)

        for symbol in momentum_rank.columns:
            # if mon_rank[symbol] == 1, change the value to 1. Otherwise, change it to 0.
            momentum_rank[symbol] = np.where(momentum_rank[symbol] == 1, 1, 0)
        return momentum_rank

    def decision(self):
        # Investment decision based on strategy algorithm
        if (self.mom_rank.iloc[-1] == 0).all():
            # if all scores are zero, hold cash
            allocate = {'Asset': ['Cash'], 'Weight (%)': [100]}
            allocate_df = pd.DataFrame(allocate)
            allocate_df.set_index('Asset', inplace=True)
            return allocate_df
        else:
            invest = self.mom_rank.columns[(self.mom_rank == 1).iloc[-1]][0]
            allocate = {'Asset': [invest], 'Description': [], 'Weight (%)': [
                100]}
            for asset in allocate['Asset']:
                desc = yf.Ticker(asset).info[0]['longName']
                allocate['Description'].append(desc)
            allocate_df = pd.DataFrame(allocate)
            allocate_df.set_index('Asset', inplace=True)
            return allocate_df

    def monthly_return(self):
        monthly_returns = self.prices.pct_change()
        monthly_returns.dropna(inplace=True)
        return monthly_returns

    def cumulative_return(self):
        # we have to shift the returns upward by one to align with momentum signal above.
        monthly_returns = self.monthly_return()
        monthly_returns = monthly_returns[self.mom_rank.index[0]:].shift(-1)
        vaa_port_returns = np.multiply(
            self.mom_rank, monthly_returns).sum(axis=1)
        vaa_port_cum_returns = np.exp(np.log1p(vaa_port_returns).cumsum())[:-1]
        return vaa_port_cum_returns

    def cagr(self):
        first_value = self.port_cum_returns[0]
        last_value = self.port_cum_returns[-1]
        years = len(self.port_cum_returns.index)/12
        cagr = (last_value/first_value)**(1/years) - 1
        return cagr

    def mdd(self):
        previous_peaks = self.port_cum_returns.cummax()
        drawdown = (self.port_cum_returns - previous_peaks) / previous_peaks
        port_mdd = drawdown.min()
        return port_mdd


if __name__ == "__main__":
    vaa = VAA()
    vaa.decision()
    print(vaa.monthly_return())
