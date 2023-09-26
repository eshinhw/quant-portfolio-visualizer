from BasePortfolio import BasePortfolio
import pandas as pd
import numpy as np


class MomentumPortfolio(BasePortfolio):
    def port_cum_returns(self):
        monthly_momentum = self.monthly_momentum()
        rank_df = monthly_momentum.rank(axis=1, ascending=False)
        for col in rank_df.columns:
            rank_df[col] = np.where(rank_df[col] == 1, 1, 0)

        monthly_returns = self.monthly_returns()
        monthly_returns = monthly_returns[rank_df.index[0] :].shift(-1)

        port = np.multiply(rank_df, monthly_returns)
        port_returns = port.sum(axis=1)
        port_cum_returns = np.exp(np.log1p(port_returns).cumsum())[:-1]
        return port_cum_returns

    def monthly_momentum(self):
        monthly_prices = self.monthly_prices()
        monthly_momentum = monthly_prices.copy().apply(lambda x: x.shift(1) / x.shift(12) - 1, axis=0)
        monthly_momentum.dropna(inplace=True)
        return monthly_momentum


if __name__ == "__main__":
    mp = MomentumPortfolio()
