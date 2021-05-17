import secret
import requests
from typing import List, Dict

from pytickersymbols import PyTickerSymbols

"""
GET list of S&P 500 symbols (financialmodelingprep API)
"""

def get_sp500_symbols(index: str) -> Dict:
    data = {}
    pyticker = PyTickerSymbols()
    try:
        sp500 = list(pyticker.get_stocks_by_index(index))
    except:
        print('index not valid')
        return

    for record in sp500:
        symbol = record['symbol']
        sector = record['industries'][0]
        name = record['name']
        data[symbol] = {}
        data[symbol]['name'] = name
        data[symbol]['sector'] = sector

    return data



api = secret.FMP_API_KEYS

sp500 = requests.get(f'https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={api}').json()




"""
CALCULATE historical momentum (yahoo finance)
1. calculate historical monthly prices for each stock
2. momentum: Average (1,3,5,10)
"""

# def calculate_equal_weight_momentum(symbol: str, periods: List[int], start_date=None, end_date=None):
#     # start_date = dt.datetime(1970,1,1)
#     # end_date = dt.datetime.today()
#     ret = []
#     monthly_prices = get_historical_monthly_prices(symbol)
#     for period in periods:
#         #print(period)
#         monthly_returns = monthly_prices.apply(lambda x: x/x.shift(period) - 1, axis=0)
#         monthly_returns = monthly_returns.rename(columns={'Adj_Close': 'Returns'})
#         #print(monthly_returns['Returns'].iloc[-1])
#         ret.append(monthly_returns['Returns'].iloc[-1])
#     #print(ret)
#     return sum(ret) / len(ret)

"""
GET dividend data (financialmodelingprep API)
1. Current Dividend Yield
2. Dividend Grwoth: Average (3, 5)
3. Dividend Payout
"""
