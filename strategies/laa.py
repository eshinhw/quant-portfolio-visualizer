from tokenize import Double
import yfinance as yf
from math import floor
from openpyxl import Workbook
import time
from os import path, mkdir

ASSETS = ['IWD', 'IEF', 'GLD', 'QQQ', 'SHY']
WEIGHTS = {'IWD': 0.25, 'IEF': 0.25, 'GLD': 0.25, 'QQQ': 0.25, 'SHY': 0.25} 

def num_purchase_shares(portfolio_balance: float):
    for asset in ASSETS:
        curr_price = yf.Ticker(asset).history(period="max")['Close'][-1]
        allocate_amount = portfolio_balance * WEIGHTS[asset]
        shares = floor(allocate_amount / curr_price)
        print(asset, curr_price, shares)



if __name__ == "__main__":
    num_purchase_shares()
    report_to_excel()

