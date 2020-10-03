import streamlit as st
import pandas as pd
import calculator
import questrade as qt
import sys

import portfolios

import datetime as dt

ACCOUNT_NUM = '51802566'

class model_portfolio():
    
    def __init__(self, name, target):
        
        self.name = name
        self.target = target
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
        
    def rebalancing_summary(self):
        
        st.subheader('Portfolio Rebalancing Summary')
        
        cal = calculator.portfolio_rebalancing_calculator(self.target, ACCOUNT_NUM)
   
        df = cal.target_positions()    
        final, remaining_cash = cal.order_calculation(df)
        st.table(final.style.format("{:.2f}"))        
        
        st.write("POST REBALANCING CASH BALANCE: $ {:.2f} ".format(remaining_cash))

            
            
            
            
            
            
            