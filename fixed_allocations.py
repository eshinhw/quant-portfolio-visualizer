### 60/40 Benchmark

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import fmp.fmp_prices as FMP_PRICES

class FixedAllocation():

    def __init__(self,name,assets,weights) -> None:
        self.name = name
        self.assets = assets
        #['VTI', 'TLT', 'IEF', 'GLD', 'DBC']
        self.weights = weights
        #np.array([0.3, 0.4, 0.15, 0.075, 0.075])
        self.port_cum_returns = self.cumulative_returns()

    def __str__(self) -> str:
        return self.name

    def monthly_return(self):
        monthly_prices = pd.DataFrame()
        for asset in self.assets:
            monthly_prices[asset] = FMP_PRICES.get_monthly_prices(asset)[asset]
        monthly_returns = monthly_prices.pct_change()
        monthly_returns.dropna(inplace=True)
        return monthly_returns

    def cumulative_returns(self):
        prices = pd.DataFrame() 

        for symbol in self.assets:
            prices[symbol] = FMP_PRICES.get_monthly_prices(symbol)[symbol]

        prices.dropna(inplace=True)
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

class AllWeather():

    def __init__(self) -> None:
        self.assets = ['VT', 'LTPZ', 'EDV', 'VCLT', 'EMLC', 'IAU', 'BCI']
        self.weights = np.array([0.35, 0.2, 0.2, 0.075, 0.075, 0.05, 0.05])
        self.port_cum_returns = self.cumulative_returns()

    def __str__(self) -> str:
        return "All Weather"

    def monthly_return(self):
        monthly_prices = pd.DataFrame()
        for asset in self.assets:
            monthly_prices[asset] = FMP_PRICES.get_monthly_prices(asset)[asset]
        monthly_returns = monthly_prices.pct_change()
        monthly_returns.dropna(inplace=True)
        return monthly_returns

    def cumulative_returns(self):
        prices = pd.DataFrame() 

        for symbol in self.assets:
            prices[symbol] = FMP_PRICES.get_monthly_prices(symbol)[symbol]

        prices.dropna(inplace=True)
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

class Permanent():
    def __init__(self) -> None:
        self.assets = ['VTI', 'IEF', 'TLT', 'GLD']
        self.weights = np.array([0.25, 0.25, 0.25, 0.25])
        self.port_cum_returns = self.cumulative_returns()

    def __str__(self) -> str:
        return "Permanent"

    def monthly_return(self):
        monthly_prices = pd.DataFrame()
        for asset in self.assets:
            monthly_prices[asset] = FMP_PRICES.get_monthly_prices(asset)[asset]
        monthly_returns = monthly_prices.pct_change()
        monthly_returns.dropna(inplace=True)
        return monthly_returns

    def cumulative_returns(self):
        prices = pd.DataFrame() 

        for symbol in self.assets:
            prices[symbol] = FMP_PRICES.get_monthly_prices(symbol)[symbol]

        prices.dropna(inplace=True)
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

class SixtyForty():

    def __init__(self) -> None:
        self.assets = ['BND', 'SPY']
        self.weights = np.array([0.4, 0.6])
        self.port_cum_returns = self.cumulative_returns()

    def __str__(self) -> str:
        return "60 Stocks / 40 Bonds"

    def monthly_return(self):
        monthly_prices = pd.DataFrame()
        for asset in self.assets:
            monthly_prices[asset] = FMP_PRICES.get_monthly_prices(asset)[asset]
        monthly_returns = monthly_prices.pct_change()
        monthly_returns.dropna(inplace=True)
        return monthly_returns

    def cumulative_returns(self):
        prices = pd.DataFrame() 

        for symbol in self.assets:
            prices[symbol] = FMP_PRICES.get_monthly_prices(symbol)[symbol]

        prices.dropna(inplace=True)
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

    def __str__(self) -> str:
        return "100% SPY"

    def monthly_return(self):
        monthly_prices = pd.DataFrame()
        for asset in self.assets:
            monthly_prices[asset] = FMP_PRICES.get_monthly_prices(asset)[asset]
        monthly_returns = monthly_prices.pct_change()
        monthly_returns.dropna(inplace=True)
        return monthly_returns

    def cumulative_returns(self):
        prices = pd.DataFrame() 

        for symbol in self.assets:
            prices[symbol] = FMP_PRICES.get_monthly_prices(symbol)[symbol]

        prices.dropna(inplace=True)
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

if __name__ == "__main__":
    # sf = SixtyForty()

    # spy = SPY()

    fs = FourSeasons()

    # print(sf.cagr(), sf.mdd())
    # print(spy.cagr(), spy.mdd())
    print(fs.cagr(), fs.mdd())
