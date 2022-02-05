"""
Vigilant Asset Allocation (VAA) Implementation Source Codes
"""

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import fmp.fmp_prices as FMP_PRICES

class VAA():

    def __init__(self) -> None:
        self.offensive_assets = ['SPY', 'VEA', 'VWO', 'AGG']
        self.defensive_assets = ['SHY', 'IEF', 'LQD']
        self.momentum_periods = [1,3,6,12]
        self.momentum_weights = np.array([12,4,2,1])



    def _price(self):

        total_assets = self.offensive_assets + self.defensive_assets

        print(total_assets)

        self.total_monthly_prices = pd.DataFrame()

        for asset in total_assets:
            self.total_monthly_prices[asset] = FMP_PRICES.get_monthly_prices(asset)[asset]

        self.total_monthly_prices.dropna(inplace=True)

        print(self.total_monthly_prices)

        def mom_score(x):
            m1 = x / x.shift(1) - 1
            m3 = x / x.shift(3) - 1
            m6 = x / x.shift(6) - 1
            m12 = x / x.shift(12) - 1
            return 12 * m1 + 4 * m3 + 2 * m6 + 1 * m12

        # calcuate weighted momentum scores at each month
        self.total_monthly_mom = self.total_monthly_prices.copy().apply(mom_score,axis=0)
        self.total_monthly_mom.dropna(inplace=True)

        print(self.total_monthly_mom)

        print("CHECK CONDITIONS")

        for date in self.total_monthly_mom.index:
            if (self.total_monthly_mom.loc[date,['SPY', 'VEA', 'VWO', 'AGG']] < 0).any():
                # check defensive assets
                self.total_monthly_mom.loc[date, 'SPY'] = 0
                self.total_monthly_mom.loc[date, 'VEA'] = 0
                self.total_monthly_mom.loc[date, 'VWO'] = 0
                self.total_monthly_mom.loc[date, 'AGG'] = 0
                if (self.total_monthly_mom.loc[date,['SHY', 'IEF', 'LQD']] < 0).any():
                    # hold cash
                    self.total_monthly_mom.loc[date, 'SHY'] = 0
                    self.total_monthly_mom.loc[date, 'IEF'] = 0
                    self.total_monthly_mom.loc[date, 'LQD'] = 0
            else:
                # invest offensive asset
                self.total_monthly_mom.loc[date, 'SHY'] = 0
                self.total_monthly_mom.loc[date, 'IEF'] = 0
                self.total_monthly_mom.loc[date, 'LQD'] = 0
        
        print(self.total_monthly_mom)

        print("AFTER CHECKING CONDITIONS")

        # rank across columns
        mom_rank = self.total_monthly_mom.rank(axis=1, ascending=False)

        for symbol in mom_rank.columns:
            # if mon_rank[symbol] == 1, change the value to 1. Otherwise, change it to 0.
            mom_rank[symbol] = np.where(mom_rank[symbol] == 1, 1, 0)
        
        print(mom_rank)

        

        

        # we have to shift the returns upward by one to align with momentum signal above.
        total_monthly_returns = self.total_monthly_prices.pct_change()
        total_monthly_returns.dropna(inplace=True)
        print(total_monthly_returns)
        total_monthly_returns = total_monthly_returns[mom_rank.index[0]:].shift(-1)
        
        print(mom_rank.index[0])
        #print(total_monthly_returns[mom_rank.index[0]:])
        
        print(total_monthly_returns)


        vaa_port = np.multiply(mom_rank, total_monthly_returns)
        
        print("============================================================================")
        
        print(vaa_port)
        vaa_port_returns = vaa_port.sum(axis=1)

        print(vaa_port_returns)
        
        vaa_port_cum_returns = np.exp(np.log1p(vaa_port_returns).cumsum())[:-1]

        print(vaa_port_cum_returns)


        # print(total_monthly_returns)

    def _weighted_momentum(self):
        ## Offensive assets momentum

        offensive_momentum_data = {'1M': [], '3M': [], '6M': [], '12M': []}
        for symbol in self.offensive_assets:
            for period in self.momentum_periods:        
                offensive_momentum_data[str(period)+'M'].append(FMP_PRICES.historical_monthly_momentum(symbol,period))
        self.offensive_momentum = pd.DataFrame(offensive_momentum_data, index=self.offensive_assets)
        self.offensive_momentum['Score'] = self.offensive_momentum.dot(self.momentum_weights)

        print(self.offensive_momentum)

        ## Defensive Assets Momentum

        defensive_momentum_data = {'1M': [], '3M': [], '6M': [], '12M': []}

        for symbol in self.defensive_assets:
            for period in self.momentum_periods:        
                defensive_momentum_data[str(period)+'M'].append(FMP_PRICES.historical_monthly_momentum(symbol,period))

        self.defensive_momentum = pd.DataFrame(defensive_momentum_data, index=self.defensive_assets)
        self.defensive_momentum['Score'] = self.defensive_momentum.dot(self.momentum_weights)

        print(self.defensive_momentum)

    def decision(self):
        ## Investment decision based on strategy algorithm

        if (self.offensive_momentum['Score'] < 0).any():
            if (self.defensive_momentum['Score'] < 0).any():
                print('hold cash')
            else:
                first = self.defensive_momentum.sort_values(by='Score', ascending=False).index[0]
                print('invest in ' + first)
        else:
            first = self.offensive_momentum.sort_values(by='Score', ascending=False).index[0]
            print('invest in ' + first)

    def cumulative_return(self):
        pass

    def cagr(self):
        pass
    
    def mdd(self):
        pass

    def sharpe(self):
        pass

    # def backtesting(self):




    #     vaa_monthly_prices.head(10)


    #     vaa_monthly_mom = vaa_monthly_prices.copy()
    #     vaa_monthly_mom = vaa_monthly_mom.apply(vaa_returns, axis=0)
    #     vaa_monthly_mom.dropna(inplace=True)




vaa = VAA()

vaa._price()
# vaa._weighted_momentum()

"""






### 60/40 Benchmark
assets = ['BND', 'SPY']

sixtyForty = pd.DataFrame()

for symbol in assets:
    sixtyForty[symbol] = fmp.get_monthly_prices(symbol)[symbol]
sixtyForty_returns = sixtyForty.pct_change()
sixtyForty_returns = sixtyForty_returns[mom_rank.index[0]:].shift(-1)
sixtyForty_weights = np.array([0.4, 0.6])
sixtyForty_returns['port'] = sixtyForty_returns.dot(sixtyForty_weights)
sixtyForty_returns.tail()
sixtyForty_cum_returns = np.exp(np.log1p(sixtyForty_returns['port']).cumsum())[:-1]
sixtyForty_cum_returns.tail()

### SPY (S&P 500)
benchmark_prices = fmp.get_monthly_prices('SPY')
benchmark_returns = benchmark_prices.pct_change()
benchmark_returns = benchmark_returns[mom_rank.index[0]:].shift(-1)
benchmark_cum_returns = np.exp(np.log1p(benchmark_returns).cumsum())[:-1]
benchmark_cum_returns.tail()
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
### Backtesting Performance Comparison (All Portfolios)
plt.figure(figsize=(15,10))
plt.plot(combined_df)
plt.legend(combined_df.columns)
plt.xlabel('Date')
plt.ylabel('Returns')
plt.title('Portfolio Performance Comparison')
### Backtesting Performance Comparison (Original VAA, 60/40, SPY)
sub_df = combined_df[['VAA/Original', '60/40', 'SPY']]
plt.figure(figsize=(15,10))
plt.plot(sub_df)
plt.legend(sub_df.columns)
plt.xlabel('Date')
plt.ylabel('Returns')
plt.title('Portfolio Performance Comparison')



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