import sys

from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(d)

import datetime as dt
from genericpath import getmtime
import math
import os
import platform
import pprint
import time

import pandas as pd
import requests
from qtrade import Questrade

class QuestradeBot:
    def __init__(self, token) -> None:

        self.token = token

        if os.path.exists("./access_token.yml"):
            try:
                self.Questrade = Questrade(token_yaml="./access_token.yml")
                self.Questrade.refresh_access_token(from_yaml=True)
            except Exception as e:
                os.remove("./access_token.yml")
                print(e)
        else:
            self.Questrade = Questrade(access_code=self.token)

            # check expired
            # modified = dt.datetime.fromtimestamp(os.path.getmtime("./access_token.yml"))
            # now = dt.datetime.now()
            # fileAge = (now - modified).days
            # if fileAge > 3:
            #     print("fileAge part executed")
            #     print("access_token.yml EXPIRED: REFRESH QUESTRADE API TOKEN")
            #     os.remove("./access_token.yml")
            # else:
            #     # we can refresh token
            #     print("refresh_token")
            #     self.Questrade = Questrade(token_yaml="./access_token.yml")
            #     self.Questrade.refresh_access_token(from_yaml=True)

        # if not (os.path.exists("./access_token.yml")):
            # self.Questrade = Questrade(access_code=self.token)

    # def get_account_ids(self):
    #     return self.Questrade.get_account_id()

    def get_acct_positions(self, acctNum):
        return self.Questrade.get_account_positions(acctNum)

    def get_ticker_info(self, symbol: str):
        return self.Questrade.ticker_information(symbol)

    def get_balance(self, acctNum):
        token = self.Questrade.access_token
        token_type = token['token_type']
        access_token = token['access_token']
        url = token['api_server'] + '/v1/accounts/' + str(acctNum) + '/balances'
        bal = requests.get(url, headers={'Authorization': f'{token_type} {access_token}'}).json()

        data = {'Currency': [], 'Cash': [], 'Market_Value': [], 'Total_Equity': [], 'Cash (%)': [], 'Investment (%)': []}

        for x in bal['perCurrencyBalances']:
            data['Currency'].append(x['currency'])
            data['Cash'].append(x['cash'])
            data['Market_Value'].append(x['marketValue'])
            data['Total_Equity'].append(x['totalEquity'])
            if x['totalEquity'] != 0:
                data['Cash (%)'].append(round(100 * x['cash']/x['totalEquity'],2))
                data['Investment (%)'].append(round(100 * x['marketValue']/x['totalEquity'],2))
            else:
                data['Cash (%)'].append(0)
                data['Investment (%)'].append(0)

        df = pd.DataFrame(data)
        df.set_index('Currency', inplace=True)
        return df

    def search_symbolID(self, symbol: str):
        # https://api01.iq.questrade.com/v1/symbols/search?prefix=BMO
        token = self.Questrade.access_token
        token_type = token['token_type']
        access_token = token['access_token']
        url = token['api_server'] + '/v1/symbols/search?prefix=' + symbol
        resp = requests.get(url, headers={'Authorization': f'{token_type} {access_token}'}).json()
        symbolID = resp['symbols'][0]['symbolId']
        return symbolID

    def get_option_chains(self, symbol: str):
        # https://api01.iq.questrade.com/v1/symbols/9291/options
        token = self.Questrade.access_token
        token_type = token['token_type']
        access_token = token['access_token']
        sID = self.search_symbolID(symbol)
        url = token['api_server'] + '/v1/symbols/' + str(sID) + '/options'
        resp = requests.get(url, headers={'Authorization': f'{token_type} {access_token}'}).json()
        return resp

    def get_id_details(self, sID: int):
        # v1/markets/quotes/
        token = self.Questrade.access_token
        token_type = token['token_type']
        access_token = token['access_token']
        url = token['api_server'] + '/v1/markets/quotes/' + str(sID)
        resp = requests.get(url, headers={'Authorization': f'{token_type} {access_token}'}).json()
        return resp

    def create_option_chains(self, symbol, callID, putID):
        opt_chains = self.get_option_chains(symbol)
        print(opt_chains['optionChain'][0])


    def get_usd_total_equity(self, acctNum):
        balance = self.get_balance(acctNum)
        return balance.loc['USD','Total_Equity']

    def get_usd_total_mv(self, acctNum):
        balance = self.get_balance(acctNum)
        return balance.loc['USD', 'Market_Value']

    def get_cad_total_equity(self, acctNum):
        balance = self.get_balance(acctNum)
        return balance.loc['CAD','Total_Equity']

    def get_cad_total_mv(self, acctNum):
        balance = self.get_balance(acctNum)
        return balance.loc['CAD', 'Market_Value']

    def get_usd_total_cost(self, acctNum):
        positions = self.get_acct_positions(acctNum)
        total_cost = 0
        for pos in positions:
            curr_cost = pos['totalCost']
            total_cost += curr_cost
        return total_cost

    def get_investment_summary(self, acctNum):
        position_data = {
            'Symbol': [],
            'Description': [],
            'Currency': [],
            'Quantities': [],
            'Market Value': [],
            'Return (%)': [],
            'Portfolio (%)': []
        }
        total_market_value = self.get_usd_total_mv(acctNum)
        total_costs = 0
        positions = self.Questrade.get_account_positions(acctNum)
        for position in positions:
            # handle daily execution for closeQuantity
            if position['openQuantity'] != 0:
                symbol = position['symbol']
                description = self.Questrade.ticker_information(symbol)['description']
                qty = position['openQuantity']
                cmv = position['currentMarketValue']
                currency = self.Questrade.ticker_information(symbol)['currency']
                cost = position['totalCost']
                change = round(100 * (cmv - cost) / cost, 2)

                total_costs = total_costs + cost
                position_data['Symbol'].append(symbol)
                position_data['Description'].append(description)
                position_data['Currency'].append(currency)
                position_data['Quantities'].append(qty)
                position_data['Market Value'].append(cmv)
                position_data['Return (%)'].append(change)
                position_data['Portfolio (%)'].append(round(100 * (cmv / total_market_value),2))

        portfolio = pd.DataFrame(position_data)
        portfolio.set_index('Symbol', inplace=True)
        portfolio.index.name = None
        return portfolio

    def get_dividend_income(self, acctNum):
        startDate = '2018-04-01'
        endDate = dt.date.today().strftime("%Y-%m-%d")
        dtrange = pd.date_range(startDate, endDate, freq='d')
        months = pd.Series(dtrange.month)
        starts, ends = months.ne(months.shift(1)), months.ne(months.shift(-1))
        startEndDates = pd.DataFrame({
            'month_starting_date':
            dtrange[starts].strftime('%Y-%m-%d'),
            'month_ending_date':
            dtrange[ends].strftime('%Y-%m-%d')
        })
        dateList = startEndDates.values.tolist()

        output = {}
        total_div_earned = 0

        for date in dateList:
            start = date[0]
            end = date[1]
            activities = self.Questrade.get_account_activities(acctNum, start, end)
            monthly_div = 0
            for activity in activities:
                if activity['type'] == 'Dividends':
                    monthly_div = monthly_div + activity['netAmount']
            output[dt.datetime.strptime(start,
                                        "%Y-%m-%d").strftime("%Y-%m")] = monthly_div
            total_div_earned = total_div_earned + monthly_div

        monthly_div_df = pd.DataFrame.from_dict(output,
                                            orient='index',
                                            columns=['Monthly_Dividend_Income'])

        return monthly_div_df

    def calculate_portfolio_return(self, acctNum):
        total_mv = self.get_usd_total_mv(acctNum)
        total_cost = self.get_usd_total_cost(acctNum)
        m1 = round(100 * (total_mv - total_cost) / total_cost, 2)

        investment = self.get_investment_summary(acctNum)

        m2 = 0
        for symbol in investment.index:

            ret = investment.loc[symbol, 'Return (%)']
            port = investment.loc[symbol, 'Portfolio (%)'] / 100

            m2 += ret * port

        print(m1, m2)

# def calculate_shares(symbol: str, weight: float, currency: str):
#     total_equity = qbot.get_usd_total_equity()
#     amount = total_equity * weight
#     curr_price = get_daily_prices(symbol)
#     return (amount, math.floor(amount / curr_price))

