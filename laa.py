import yfinance as yf
from math import floor

ASSETS = ['IWD', 'IEF', 'GLD', 'QQQ', 'SHY']
WEIGHTS = {'IWD': 0.25, 'IEF': 0.25, 'GLD': 0.25, 'QQQ': 0.25, 'SHY': 0.25} 
ACCOUNT_BALANCE = 3000

def num_purchase_shares(asset: str):
    curr_price = yf.Ticker(asset).history(period="max")['Close'][-1]
    allocate_amount = ACCOUNT_BALANCE * WEIGHTS[asset]
    return floor(allocate_amount / curr_price)

for asset in ASSETS:
    shares = num_purchase_shares(asset)
    print(asset, shares)
