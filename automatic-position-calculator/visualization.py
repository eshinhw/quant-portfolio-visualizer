import streamlit as st
import pandas as pd
import calculator
import questrade as qt
import sys

import portfolios


st.title("**Portfolio Rebalancing Calculator**")

st.sidebar.header('User Input')

accountNum = st.sidebar.text_input('Enter Your Questrade Account Number')

if st.sidebar.button('Submit'):
    st.sidebar.success("Submitted!")

st.sidebar.header('Model Portfolios')

if st.sidebar.checkbox('Balanced Portfolio'):

    name1 = 'Balanced Portfolio' 
   
    st.header('Selected Portfolio: ' + name1)  
    
    st.subheader('Portfolio Holdings')
    
    target = {'VFV.TO': 0.5, 'XBB.TO': 0.5}
    
    description = portfolios.get_description(target)    
    input_dict = {'Symbol':[], 'Symbol Description':[], 'Weight':[]}
    
    for d in description:
        input_dict['Symbol'].append(d[0])
        input_dict['Symbol Description'].append(d[1])
        input_dict['Weight'].append(d[2])

    description_table = pd.DataFrame(input_dict)
    description_table.set_index('Symbol', inplace=True)
    st.table(description_table)
    
    # HISTORICAL PERFORMANCE MEASURES
    
    st.subheader('Historical Performance Measures')
    stats = portfolios.get_performance(target)
    
    measures_dict = {'Name': [name1], 'Since': [stats[0]], 'CAGR': [stats[1]], 'MDD': [stats[2]], 'Sharpe': [stats[3]]}    
        
    measures_table = pd.DataFrame(measures_dict)
    measures_table.set_index('Name', inplace=True)
    
    st.table(measures_table)
    
    # REBALANCING ORDER SUMMARY
        
    st.subheader('Rebalancing Order Summary')
    
    cal = calculator.portfolio_rebalancing_calculator(target, '51802566')
   
    df = cal.target_positions()    
    final = cal.order_calculation(df)
    st.table(final.style.format("{:.2f}"))
    
    for symbol in final.index:
        qtychange = final.loc[symbol,'Qty Change']
        price = final.loc[symbol, 'Price']
        
        if  qtychange < 0:
            st.write("SELL {} SHARES OF {} AT $ {}".format(abs(qtychange), symbol, price))
        
        if qtychange > 0:
            st.write("BUY {} SHARES OF {} AT $ {}".format(abs(qtychange), symbol, price))
            
if st.sidebar.checkbox('All Weather Portfolio'):

    name2 = 'All Weather Portfolio' 
   
    st.header('Selected Portfolio: ' + name2)  
    
    st.subheader('Portfolio Holdings')
    
    target = {'VTI': 0.3, 'TLT': 0.4, 'IEI': 0.15, 'GLD': 0.075, 'GSG': 0.075}
    
    description = portfolios.get_description(target)    
    input_dict = {'Symbol':[], 'Symbol Description':[], 'Weight':[]}
    
    for d in description:
        input_dict['Symbol'].append(d[0])
        input_dict['Symbol Description'].append(d[1])
        input_dict['Weight'].append(d[2])

    description_table = pd.DataFrame(input_dict)
    description_table.set_index('Symbol', inplace=True)
    st.table(description_table)
    
    # HISTORICAL PERFORMANCE MEASURES
    
    st.subheader('Historical Performance Measures')
    stats = portfolios.get_performance(target)
    
    measures_dict = {'Name': [name2], 'Since': [stats[0]], 'CAGR': [stats[1]], 'MDD': [stats[2]], 'Sharpe': [stats[3]]}    
        
    measures_table = pd.DataFrame(measures_dict)
    measures_table.set_index('Name', inplace=True)
    
    st.table(measures_table)
    
    # REBALANCING ORDER SUMMARY
        
    st.subheader('Rebalancing Order Summary')
    
    cal = calculator.portfolio_rebalancing_calculator(target, '51802566')
   
    df = cal.target_positions()    
    final = cal.order_calculation(df)
    st.table(final.style.format("{:.2f}"))
    
    for symbol in final.index:
        qtychange = final.loc[symbol,'Qty Change']
        price = final.loc[symbol, 'Price']
        
        if  qtychange < 0:
            st.write("SELL {} SHARES OF {} AT $ {}".format(abs(qtychange), symbol, price))
        
        if qtychange > 0:
            st.write("BUY {} SHARES OF {} AT $ {}".format(abs(qtychange), symbol, price))
    
