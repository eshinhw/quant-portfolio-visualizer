import os
import math
import requests
import momentum
import pyticker
import dividend
import questrade
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from qtrade import Questrade as qt
import pandas_datareader.data as web

if os.path.exists("./access_token.yml"):
    qtrade = qt(token_yaml="./access_token.yml")
    qtrade.refresh_access_token(from_yaml=True)
else:
    code = open("./credentials/questrade_access_code.txt", "r").read()
    qtrade = qt(access_code=code)


def get_balance():
    token = qtrade.access_token
    token_type = token['token_type']
    access_token = token['access_token']
    acctId = qtrade.get_account_id()
    url = token['api_server'] + '/v1/accounts/' + acctId[0] + '/balances'
    bal = requests.get(url, headers={'Authorization': f'{token_type} {access_token}'}).json()
    data = {'Currency': [], 'Cash': [], 'Market_Value': [], 'Total_Equity': []}

    for x in bal['perCurrencyBalances']:
        data['Currency'].append(x['currency'])
        data['Cash'].append(x['cash'])
        data['Market_Value'].append(x['marketValue'])
        data['Total_Equity'].append(x['totalEquity'])

    df = pd.DataFrame(data)
    df.set_index('Currency', inplace=True)
    return df

def get_positions():
    position_data = {
        'Symbol': [],
        'Description': [],
        'Currency': [],
        'Quantities': [],
        'Market Value': [],
        'Gain/Loss (%)': []
    }
    total_costs = 0
    total_market_value = 0
    for account in acctId:
        positions = qtrade.get_account_positions(account)
        for position in positions:
            symbol = position['symbol']
            description = qtrade.ticker_information(symbol)['description']
            qty = position['openQuantity']
            cmv = position['currentMarketValue']
            currency = qtrade.ticker_information(symbol)['currency']
            cost = position['totalCost']
            change = round(100 * (cmv - cost) / cost, 2)

            total_market_value = total_market_value + cmv
            total_costs = total_costs + cost
            position_data['Symbol'].append(symbol)
            position_data['Description'].append(description)
            position_data['Currency'].append(currency)
            position_data['Quantities'].append(qty)
            position_data['Market Value'].append(cmv)
            position_data['Gain/Loss (%)'].append(change)


if __name__ == '__main__':

    bal = get_balance_summary()
    print(bal)