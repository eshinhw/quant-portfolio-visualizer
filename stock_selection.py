import os
import json
import math
import price
import ratios
import requests
import momentum
import pyticker
import dividend
# import questrade
# import auto_email
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader.data as web

###############################################################################
# GLOBAL VARIABLES
WATCHLIST = ['O']
MOMENTUM_PERIODS = [3,6,12,24,36,48,60,72,84,96,108,120]
MARKET_CAP_THRESHOLD = 200
###############################################################################

def extract_from_sp500():

    sp500 = pyticker.get_symbols_by_index('S&P 500')

    data = {'Symbol': [], 'Market_Cap (B)': []}

    min_market_cap = MARKET_CAP_THRESHOLD

    count = 0

    for symbol in sp500:
        count += 1
        print(f"{symbol}: {count}/{len(sp500)}")
        try:
            market_cap = ratios.calculate_market_cap(symbol)
        except:
            continue

        if market_cap >= min_market_cap and dividend.exists_dividends(symbol):
            data['Symbol'].append(symbol)
            data['Market_Cap (B)'].append(market_cap)
            print(f"{symbol} has been added!")

    return data



def compare_symbol_list():

    if not os.path.exists('./symbols_selected_from_sp500.json'):
        data = extract_from_sp500()
        with open('./symbols_selected_from_sp500.json', 'w') as fp:
            json.dump(data,fp)
    else:
        with open('./symbols_selected_from_sp500.json', 'r') as fp:
            loaded_data = json.load(fp)
        new_data = extract_from_sp500()

        if not (loaded_data == new_data):
            with open('./symbols_selected_from_sp500.json', 'w') as fp:
                json.dump(new_data,fp)


###############################################################################
# Load Data
###############################################################################
def construct_stock_df_to_csv():

    compare_symbol_list()

    with open('./symbols_selected_from_sp500.json', 'r') as fp:
        data = json.load(fp)
    df = pd.DataFrame(data)
    df.set_index('Symbol', inplace=True)

    ###############################################################################
    # Update Watchlist
    ###############################################################################
    watchlist_data = {'Symbol': [], 'Market_Cap (B)': []}
    for symbol in WATCHLIST:
        if len(WATCHLIST) == 1:
            watchlist_data['Symbol'] = symbol
            watchlist_data['Market_Cap (B)'] = ratios.calculate_market_cap(symbol)
        else:
            watchlist_data['Symbol'].append(symbol)
            watchlist_data['Market_Cap (B)'].append(ratios.calculate_market_cap(symbol))

    df.reset_index(inplace=True)
    df = df.append(watchlist_data, ignore_index=True)
    df.set_index('Symbol', inplace=True)

    ###############################################################################
    # Financial Ratios Calculations
    ###############################################################################
    for symbol in list(df.index):

        try:
            div_growth = dividend.calcualte_avg_dividend_growth(symbol,10)
            df.loc[symbol, 'Dividend_Growth'] = div_growth
        except:
            df.loc[symbol, 'Dividend_Growth'] = np.nan

        try:
            div_yield = dividend.calculate_current_dividend_yield(symbol)
            df.loc[symbol, 'Dividend_Yield'] = div_yield
        except:
            df.loc[symbol, 'Dividend_Yield'] = np.nan

        try:
            mom = momentum.calculate_equal_weight_momentum(symbol, MOMENTUM_PERIODS)
            df.loc[symbol,'Momentum'] = mom
        except:
            df.loc[symbol,'Momentum'] = np.nan

    df.to_csv(r'./stock_selection.csv')








