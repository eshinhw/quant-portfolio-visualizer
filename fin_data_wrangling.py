import requests
import credentials
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web

FMP_API_KEY = credentials.FMP_API_KEYS

def sp500_symbols():
    symbols = []
    sp500 = requests.get(f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={FMP_API_KEY}").json()

    for data in sp500:
        symbols.append(data['symbol'])

    return symbols

def financials():

    symbols = sp500_symbols()

    financials_data = {'symbol': [],
                       'name': [],
                       'exchange': [],
                       'sector': [],
                       'industry': [],
                       'marketCap(B)': [],
                       'Revenue_Growth': [],
                       'ROE': [],
                       'GPMargin': [],
                       'EPS_Growth': [],
                       'DivYield': [],
                       'DPS': [],
                       'DPS_Growth': []
                       }

    for symbol in symbols[:2]:

        financials_data['symbol'].append(symbol)

        try:
            profile = requests.get(f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FMP_API_KEY}").json()[0]
            ratio_ttm = requests.get(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={FMP_API_KEY}").json()[0]
            growth = requests.get(f"https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?period=quarter&limit=20&apikey={FMP_API_KEY}").json()[0]
        except:
            continue

        financials_data['name'].append(profile['companyName'])
        financials_data['exchange'].append(profile['exchangeShortName'])
        financials_data['sector'].append(profile['sector'])
        financials_data['industry'].append(profile['industry'])
        financials_data['marketCap(B)'].append(profile['mktCap']/1000000000)
        financials_data['DivYield'].append(ratio_ttm['dividendYieldTTM'])
        financials_data['DPS'].append(ratio_ttm['dividendPerShareTTM'])
        financials_data['DPS_Growth'].append(growth['fiveYDividendperShareGrowthPerShare'])
        financials_data['ROE'].append(ratio_ttm['returnOnEquityTTM'])
        financials_data['GPMargin'].append(ratio_ttm['grossProfitMarginTTM'])
        financials_data['EPS_Growth'].append(growth['epsgrowth'])
        financials_data['Revenue_Growth'].append(growth['fiveYRevenueGrowthPerShare'])

        df_financials = pd.DataFrame(financials_data)

        df_financials.to_csv('./data/financials.csv')


if __name__ == "__main__":
    # sp500_symbols()

    historical_prices()

    # financials()