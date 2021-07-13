import requests
import credentials
import pandas as pd

FMP_API_KEY = credentials.FMP_API_KEYS

def sp500_symbols():
    symbols = []
    sp500 = requests.get(f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={FMP_API_KEY}").json()

    # print(sp500)
    for data in sp500:
        symbols.append(data['symbol'])

    print(symbols)
    # out_dict['symbols'] = symbols

    # with open(SP500_SYMBOL_PATH, 'w') as fp:
    #     json.dump(out_dict, fp)

    return symbols

def historical_prices():

    symbols = sp500_symbols()

    prices = {'symbol': [],
            'Close': [],
            'Volume': []}

    for symbol in symbols[:2]:
        price = requests.get(f"https://financialmodelingprep.com/api/v3/quote-short/{symbol.upper()}?apikey={FMP_API_KEY}").json()
        prices['symbol'].append(price[0]['symbol'])
        prices['Close'].append(price[0]['price'])
        prices['Volume'].append(price[0]['volume'])

    df_prices = pd.DataFrame(prices)
    df_prices.to_csv('./data/prices.csv')

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

    financials()