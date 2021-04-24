import streamlit as st
import streamlit_mp as mp


st.title("**Portfolio Rebalancing Calculator**")

st.sidebar.header('Model Portfolios')

if st.sidebar.checkbox('Balanced Portfolio'):

    balanced = mp.model_portfolio('Balanced Portfolio',
                                  {'VFV.TO': 0.5, 'XBB.TO': 0.5})
    balanced.description()
    balanced.performance_measures()
    balanced.rebalancing_summary()

if st.sidebar.checkbox('All Weather Portfolio'):

    allWeather = mp.model_portfolio('All Weather Portfolio',
                                    {'VTI': 0.3, 'TLT': 0.4, 'IEI': 0.15, 'GLD': 0.075, 'GSG': 0.075})
    allWeather.description()
    allWeather.performance_measures()
    allWeather.rebalancing_summary()



