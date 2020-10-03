import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt


def price(symbols):
    
    start = dt.datetime(1970,1,1)
    end = dt.datetime.today()
    
    df = pd.DataFrame()
    
    for symbol in symbols:
        
        df[symbol] = web.DataReader(symbol, 'yahoo', start, end)['Adj Close']
    
    return df

def cumulative_returns(df):
    
    daily_returns = df.pct_change()
    
    cumulative_returns = (1+daily_returns).cumprod()
    cumulative_returns.dropna(inplace=True)
    # cumulative_returns.fillna(1, inplace=True)
    
    return cumulative_returns
    

def portfolio_daily_returns(df, weights):
    pass
    

    
    
    