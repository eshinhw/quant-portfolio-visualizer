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

    def _weighted_momentum_score(self,x):
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
            monthly_prices[asset] = yf.download(asset, start= dt.datetime(2018,1,1), end = dt.datetime.today(),interval='1mo', progress=False)['Adj Close']
        monthly_prices.dropna(inplace=True)
        return monthly_prices

    def momentum_score(self):
        # calcuate weighted momentum scores at each month
        mom_score = self.prices.copy().apply(self._weighted_momentum_score,axis=0)
        mom_score.dropna(inplace=True)
        return mom_score

    def momentum_score_rank(self):

        print(self.mom_score[self.offensive_assets])
        print(self.mom_score[self.defensive_assets])
        for date in self.mom_score.index:
            if (self.mom_score.loc[date,self.offensive_assets] < 0).any():
                # check defensive assets
                self.mom_score.loc[date, 'SPY'] = float("-inf")
                self.mom_score.loc[date, 'VEA'] = float("-inf")
                self.mom_score.loc[date, 'VWO'] = float("-inf")
                self.mom_score.loc[date, 'AGG'] = float("-inf")

                # if (self.mom_score.loc[date,['SHY', 'IEF', 'LQD']] < 0).any():
                #     # hold cash
                #     self.mom_score.loc[date, 'SHY'] = 0
                #     self.mom_score.loc[date, 'IEF'] = 0
                #     self.mom_score.loc[date, 'LQD'] = 0

                #     # invest defensive asset

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
             




    # def _weighted_entumentum(self):
    #     ## Offensive assets momentum

    #     offensive_momentumentum_data = {'1M': [], '3M': [], '6M': [], '12M': []}
    #     for symbol in self.offensive_assets:
    #         for period in self.momentum_periods:        
    #             offensive_momentum_data[str(period)+'M'].append(FMP_PRICES.historical_monthly_momentum(symbol,period))
    #     self.offensive_momentum = pd.DataFrame(offensive_momentum_data, index=self.offensive_assets)
    #     self.offensive_momentum['Score'] = self.offensive_momentum.dot(self.momentum_weights)

    #     print(self.offensive_momentum)

    #     ## Defensive Assets Momentum

    #     defensive_momentum_data = {'1M': [], '3M': [], '6M': [], '12M': []}

    #     for symbol in self.defensive_assets:
    #         for period in self.momentum_periods:        
    #             defensive_momentum_data[str(period)+'M'].append(FMP_PRICES.historical_monthly_momentum(symbol,period))

    #     self.defensive_momentum = pd.DataFrame(defensive_momentum_data, index=self.defensive_assets)
    #     self.defensive_momentum['Score'] = self.defensive_momentum.dot(self.momentum_weights)

    #     print(self.defensive_momentum)

    def decision(self):
        ## Investment decision based on strategy algorithm

        print(self.mom_rank)

        if (self.offensive_momentum['Score'] < 0).any():
            if (self.defensive_momentum['Score'] < 0).all():
                print('hold cash')
            else:
                first = self.defensive_momentum.sort_values(by='Score', ascending=False).index[0]
                print('invest in ' + first)
        else:
            first = self.offensive_momentum.sort_values(by='Score', ascending=False).index[0]
            print('invest in ' + first)

    def monthly_return(self):
        monthly_returns = self.prices.pct_change()
        monthly_returns.dropna(inplace=True)
        return monthly_returns

    def cumulative_return(self):
        # we have to shift the returns upward by one to align with momentum signal above.
        monthly_returns = self.monthly_return()
        monthly_returns = monthly_returns[self.mom_rank.index[0]:].shift(-1)        
        vaa_port_returns = np.multiply(self.mom_rank, monthly_returns).sum(axis=1)      
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

"""











combined_df = pd.DataFrame()
combined_df['VAA/Original'] = vaa_port_cum_returns
combined_df['VAA/Relative_Offensive'] = offensive_port_cum_returns
combined_df['VAA/Dual_Offensive'] = dual_offensive_port_cum_returns
combined_df['60/40'] = sixtyForty_cum_returns
combined_df['SPY'] = benchmark_cum_returns
combined_df.iloc[0] = 1
combined_df.index = pd.to_datetime(combined_df.index)
combined_df
stats_summary = pd.DataFrame(columns = ['Portfolio', 'CAGR (%)', 'MDD (%)', 'CAGR/MDD'])
beginning_month = combined_df.index[0].year

for col in combined_df.columns:
    # compute CAGR
    first_value = combined_df[col][0]
    last_value = combined_df[col][-1]  
    years = len(combined_df[col].index)/12    
    cagr = (last_value/first_value)**(1/years) - 1
    
    # compute MDD
    cumulative_returns = combined_df[col]
    previous_peaks = cumulative_returns.cummax()
    drawdown = (cumulative_returns - previous_peaks) / previous_peaks
    portfolio_mdd = drawdown.min()
    
    # save CAGR and MDD for each portfolio    
    stats_summary = stats_summary.append({'Portfolio': col,
                                         'CAGR (%)': cagr * 100,
                                         'MDD (%)': portfolio_mdd * 100,
                                         'CAGR/MDD': abs(cagr / portfolio_mdd).round(2)}, ignore_index=True) 
stats_summary.set_index('Portfolio', inplace=True)
stats_summary.sort_values('CAGR/MDD', ascending=False, inplace=True)
stats_summary




"""
# ===============================================================================================
"""
### VAA (Modified: Relative Momentum Offensive Only)
#### Trading Logics


offensive_monthly_mom = offensive_monthly.copy()
offensive_monthly_mom = offensive_monthly_mom.apply(vaa_returns, axis=0)
offensive_monthly_mom.dropna(inplace=True)

# print(offensive_monthly_mom)

off_mom_rank = offensive_monthly_mom.rank(axis=1, ascending=False)
for symbol in off_mom_rank.columns:
    off_mom_rank[symbol] = np.where(off_mom_rank[symbol] < 2, 1, 0)
    
print(off_mom_rank)
    
offensive_monthly_rets = offensive_monthly.pct_change()
offensive_monthly_rets.dropna(inplace=True)
offensive_monthly_rets = offensive_monthly_rets[off_mom_rank.index[0]:].shift(-1)

offensive_port = np.multiply(off_mom_rank, offensive_monthly_rets)
offensive_port_returns = offensive_port.sum(axis=1)
offensive_port_cum_returns = np.exp(np.log1p(offensive_port_returns).cumsum())[:-1]
offensive_port_cum_returns.tail()


### VAA (Modified: Dual momentum Offensive Only)
#### Trading Logics

dual_offensive_monthly_mom = offensive_monthly.copy()
dual_offensive_monthly_mom = dual_offensive_monthly_mom.apply(vaa_returns, axis=0)
dual_offensive_monthly_mom.dropna(inplace=True)

print(dual_offensive_monthly_mom)

for date in dual_offensive_monthly_mom.index:
    if (dual_offensive_monthly_mom.loc[date] < 0).any():
        # print(date, ' negative')
        # check defensive assets
        dual_offensive_monthly_mom.loc[date, 'SPY'] = 0
        dual_offensive_monthly_mom.loc[date, 'VEA'] = 0
        dual_offensive_monthly_mom.loc[date, 'VWO'] = 0
        dual_offensive_monthly_mom.loc[date, 'AGG'] = 0

print(dual_offensive_monthly_mom)

dual_off_mom_rank = dual_offensive_monthly_mom.rank(axis=1, ascending=False)

print(dual_off_mom_rank)
for symbol in dual_off_mom_rank.columns:
    dual_off_mom_rank[symbol] = np.where(dual_off_mom_rank[symbol] == 1, 1, 0)
    
dual_offensive_monthly_rets = offensive_monthly.pct_change()
dual_offensive_monthly_rets.dropna(inplace=True)
dual_offensive_monthly_rets = dual_offensive_monthly_rets[dual_off_mom_rank.index[0]:].shift(-1)

dual_offensive_port = np.multiply(dual_off_mom_rank, dual_offensive_monthly_rets)
dual_offensive_port_returns = dual_offensive_port.sum(axis=1)
dual_offensive_port_cum_returns = np.exp(np.log1p(dual_offensive_port_returns).cumsum())[:-1]
dual_offensive_port_cum_returns

"""