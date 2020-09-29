import streamlit as st
import pandas as pd
from PIL import Image

import quant_helper as qh

import pandas as pd
import pandas_datareader.data as web
import datetime as dt

start = dt.datetime(1970,1,1)
end = dt.datetime.today()
df = pd.DataFrame()  


st.title("**Portfolio Performance Tracker**")

selected = []

st.sidebar.header('Portfolios')

if st.sidebar.checkbox('S&P 500 Benchmark'):
    selected.append('SPY')

    
if st.sidebar.checkbox('MSFT'):
    selected.append('IEF')
    
    
    
df = qh.get_price(selected)

cumulative = qh.get_cumulative_returns(df)

st.dataframe(cumulative)




    
st.line_chart(cumulative)
    
    

    
st.sidebar.header('Date Range')

start_date = st.sidebar.text_input('Start Date', '1970-01-01')
end_date = st.sidebar.text_input('End Date', dt.datetime.today().strftime('%Y-%m-%d'))

st.line_chart()