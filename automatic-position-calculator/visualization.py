import streamlit as st
import pandas as pd
import calculator
import questrade as qt



st.title("**Portfolio Performance Tracker**")

st.sidebar.header('Portfolios')

if st.sidebar.checkbox('S&P 500 Benchmark'):
    acctNum = qt.get_account_num()[0]
    
    target = {'VFV.TO': 0, 'XBB.TO': 1}
    cal = calculator.portfolio_rebalancing_calculator(target, acctNum)

    if cal.valid_input() == True:    
        df = cal.target_positions()    
        final = cal.order_calculation(df)
    st.dataframe(final)