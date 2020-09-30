import streamlit as st
import pandas as pd
import calculator
import questrade as qt
import sys


st.title("**Portfolio Rebalancing Calculator**")

st.sidebar.header('User Input')

accountNum = st.sidebar.text_input('Enter Your Questrade Account Number', type='password')

if st.sidebar.button('Submit'):
    result = accountNum.title()
    st.sidebar.success(result)

st.sidebar.header('Model Portfolios')

if st.sidebar.checkbox('Balanced Portfolio'):
    
    st.subheader('Balanced Portfolio')
    
    target = {'VFV.TO': 0.5, 'XBB.TO': 0.5}
    cal = calculator.portfolio_rebalancing_calculator(target, '51802566')
   
    df = cal.target_positions()    
    final = cal.order_calculation(df)
    st.dataframe(final.style.format("{:.2f}"))
    # st.dataframe(final)

if st.sidebar.checkbox('Crisis 100% Cash Portfolio'):
    
    st.subheader('Crisis 100% Cash Portfolio')
    
    target = {}
    cal = calculator.portfolio_rebalancing_calculator(target, '51802566')
   
    df = cal.target_positions()    
    final = cal.order_calculation(df)
    st.dataframe(final.style.format("{:.2f}"))
    # st.dataframe(final)
    





if __name__ == '__main__':
    sys.argv = ['streamlit', 'run', 'visualization.py']
