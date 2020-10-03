import streamlit as st
import pandas as pd
import calculator
import questrade as qt
import sys

import pandas_datareader.data as web
import quant_func as qf

import portfolios

import datetime as dt

ACCOUNT_NUM = '51802566'

class model_portfolio():
    
    def __init__(self, name, target):
        
        self.name = name
        self.target = target
        self.symbols = list(target.keys())
        self.weights = list(target.values())
        st.header("Selected Portfolio: " + name)        
    
    def description(self):  
        
        st.subheader('Portfolio Description')
    
        description = portfolios.get_description(self.target)    
        input_dict = {'Symbol':[], 'Symbol Description':[], 'Weight':[]}
        
        for d in description:
            input_dict['Symbol'].append(d[0])
            input_dict['Symbol Description'].append(d[1])
            input_dict['Weight'].append(d[2])
        
        description_table = pd.DataFrame(input_dict)
        description_table.set_index('Symbol', inplace=True)
        st.table(description_table)
    
    def performance_measures(self):
        
        today = dt.datetime.today().strftime('%B %d, %Y')        
        
        st.subheader('Historical Performance Measures as of ' + today)
        stats = portfolios.get_performance(self.target)
        
        measures_dict = {'Name': [self.name], 'Since': [stats[0]], 'CAGR': [stats[1]], 'MDD': [stats[2]], 'Sharpe': [stats[3]]}    
            
        measures_table = pd.DataFrame(measures_dict)
        measures_table.set_index('Name', inplace=True)
        
        st.table(measures_table)
        
    # def benchmark_comparison(self):
        
    #     START_DATE = dt.datetime(1970,1,1)
    #     END_DATE = dt.datetime.today()
        
    #     prices = pd.DataFrame()
    #     assetList = ['SPY'] + self.symbols
        
    #     for symbol in assetList:
            
    #         prices[symbol] = web.DataReader(symbol,'yahoo', START_DATE, END_DATE)['Adj Close']
            
    #     prices.dropna(inplace=True)
        
    #     cumulative = qf.cumulative_returns(prices)
        
    #     weights = np.array(self.weights)
    #     cumulative['portfolio'] = np.
        
    #     return prices, cumulative
        
        
            
        
        
        
        
        
        
    def rebalancing_summary(self):
        
        st.subheader('Portfolio Rebalancing Summary')
        
        cal = calculator.portfolio_rebalancing_calculator(self.target, ACCOUNT_NUM)
   
        df = cal.target_positions()    
        final, remaining_cash = cal.order_calculation(df)
        st.table(final.style.format("{:.2f}"))        
        
        st.write("POST REBALANCING CASH BALANCE: $ {:.2f} ".format(remaining_cash))
        

if __name__ == '__main__':
    
    balanced = model_portfolio('Balanced Portfolio', 
                                  {'VFV.TO': 0.5, 'XBB.TO': 0.5})   
    
    p, cum = balanced.benchmark_comparison()

            
            
            
            
            
            
            