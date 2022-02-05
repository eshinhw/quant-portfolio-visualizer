### 60/40 Benchmark

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import fmp.fmp_prices as FMP_PRICES

class SixtyForty():

    def __init__(self) -> None:
        self.assets = ['BND', 'SPY']
        self.weights = np.array([0.4, 0.6])
        self.port_cum_returns = self.cumulative_returns()

    def cumulative_returns(self):
        prices = pd.DataFrame() 

        for symbol in self.assets:
            prices[symbol] = FMP_PRICES.get_monthly_prices(symbol)[symbol]

        monthly_returns = prices.pct_change()
        monthly_returns = monthly_returns.shift(-1)
        monthly_returns['port'] = monthly_returns.dot(self.weights)
        cum_returns = np.exp(np.log1p(monthly_returns['port']).cumsum())[:-1]
        return cum_returns

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


class SPY():
    def __init__(self) -> None:
        self.assets = ['SPY']
        self.weights = np.array([1])
        self.port_cum_returns = self.cumulative_returns()

    def cumulative_returns(self):
        prices = pd.DataFrame() 

        for symbol in self.assets:
            prices[symbol] = FMP_PRICES.get_monthly_prices(symbol)[symbol]

        monthly_returns = prices.pct_change()
        monthly_returns = monthly_returns.shift(-1)
        monthly_returns['port'] = monthly_returns.dot(self.weights)
        cum_returns = np.exp(np.log1p(monthly_returns['port']).cumsum())[:-1]
        return cum_returns

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


sf = SixtyForty()

spy = SPY()

print(sf.cagr(), sf.mdd())
print(spy.cagr(), spy.mdd())
