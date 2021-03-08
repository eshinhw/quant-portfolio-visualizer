import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt

def get_daily_price_data(symbol, start_date, end_date):
    start = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end = dt.datetime.strptime(end_date, '%Y-%m-%d')

    df = web.DataReader(symbol, 'yahoo', start, end)
    print(df)

    return df

def get_daily_adj_close_price(df):
    price_df = df.loc[:,['Date', 'Adj Close']].copy()
    return price_df

# def get_monthly_price(price_df):
#     price_df['STD_YM'] = price_df['Date'].map(lambda x : dt.datetime.strptime(x,'%Y-%m-%d').strftime('%Y-%m'))
#     month_list = price_df['STD_YM'].unique()
#     month_last_df = pd.DataFrame()
#     for m in month_list:
#         month_last_df = month_last_df.append(
#                         price_df.loc[price_df[price_df['STD_YM']=m].index[-1], :])
#         )

def get_price_and_return_data(symbol, start_date, end_date):

    start = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end = dt.datetime.strptime(end_date, '%Y-%m-%d')

    df = pd.DataFrame()

    df[symbol] = web.DataReader(symbol, 'yahoo', start, end)['Adj Close']
    df["daily_returns"] = df.pct_change()
    df["cumulative_returns"] = (1+df["daily_returns"]).cumprod()
    df["cumulative_returns"].dropna(inplace=True)
    # cumulative_returns.fillna(1, inplace=True)
    return df

def calculate_cagr(df):

    return df.iloc[-1,2] ** (252/len(df.index)) - 1

def calculate_mdd(df):
    historical_max = df.iloc[:,0].cummax()
    daily_drawdown = df.iloc[:,0] / historical_max - 1
    historical_dd = daily_drawdown.cummin()
    #print(type(historical_dd))
    return historical_dd.min()

def calculate_vol(df):

    return np.std(df.iloc[:,1]) * np.sqrt(252)

def calculate_ex_post_sharpe(df):
    return np.mean(df.iloc[:,1]) / np.std(df.iloc[:,1]) * np.sqrt(252)










