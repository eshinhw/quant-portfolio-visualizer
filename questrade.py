import os
import math
import pprint
import requests
import credentials
import pandas as pd
import datetime as dt
from qtrade import Questrade
from utilities import get_daily_prices

class qbot:
    def __init__(self, account_num: int) -> None:
        code = credentials.QUESTRADE_API_CODE

        if os.path.exists("./access_token.yml"):
            try:
                self.qtrade = Questrade(token_yaml="./access_token.yml")
                self.acctID = self.qtrade.get_account_id()
            except:
                try:
                    self.qtrade.refresh_access_token(from_yaml=True)
                except:
                    os.remove("./access_token.yml")
                    self.qtrade = Questrade(access_code=code)
        else:
            self.qtrade = Questrade(access_code=code)

        self.acctID = account_num
        self.bal = self.get_balance()

    def get_acct_positions(self):
        return self.qtrade.get_account_positions(self.acctID)

    def get_ticker_info(self, symbol: str):
        return self.qtrade.ticker_information(symbol)

    def get_balance(self):
        token = self.qtrade.access_token
        token_type = token['token_type']
        access_token = token['access_token']
        url = token['api_server'] + '/v1/accounts/' + str(self.acctID) + '/balances'
        bal = requests.get(url, headers={'Authorization': f'{token_type} {access_token}'}).json()
        data = {'Currency': [], 'Cash': [], 'Market_Value': [], 'Total_Equity': [], 'Cash (%)': [], 'Investment (%)': []}

        for x in bal['perCurrencyBalances']:
            data['Currency'].append(x['currency'])
            data['Cash'].append(x['cash'])
            data['Market_Value'].append(x['marketValue'])
            data['Total_Equity'].append(x['totalEquity'])
            data['Cash (%)'].append(round(100 * x['cash']/x['totalEquity'],2))
            data['Investment (%)'].append(round(100 * x['marketValue']/x['totalEquity'],2))

        df = pd.DataFrame(data)
        df.set_index('Currency', inplace=True)
        return df

    def get_usd_total_equity(self):
        return self.bal.loc['USD','Total_Equity']

    def get_usd_total_mv(self):
        return self.bal.loc['USD', 'Market_Value']

    def get_cad_total_equity(self):
        return self.bal.loc['CAD','Total_Equity']

    def get_cad_total_mv(self):
        return self.bal.loc['CAD', 'Market_Value']

    def get_usd_total_cost(self):
        positions = self.get_acct_positions()
        total_cost = 0
        for pos in positions:
            curr_cost = pos['totalCost']
            total_cost += curr_cost
        return total_cost

    def get_investment_summary(self):
        position_data = {
            'Symbol': [],
            'Description': [],
            'Currency': [],
            'Quantities': [],
            'Market Value': [],
            'Return (%)': [],
            'Portfolio (%)': []
        }
        total_market_value = self.get_usd_total_mv()
        total_costs = 0
        positions = self.qtrade.get_account_positions(self.acctID)
        for position in positions:
            symbol = position['symbol']
            description = self.qtrade.ticker_information(symbol)['description']
            qty = position['openQuantity']
            cmv = position['currentMarketValue']
            currency = self.qtrade.ticker_information(symbol)['currency']
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

    def get_dividend_income(self):
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
            activities = self.qtrade.get_account_activities(self.acctID[0], start, end)
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

    def calculate_portfolio_return(self):
        total_mv = self.get_usd_total_mv()
        total_cost = self.get_usd_total_cost()
        m1 = round(100 * (total_mv - total_cost) / total_cost, 2)

        investment = self.get_investment_summary()

        m2 = 0
        for symbol in investment.index:

            ret = investment.loc[symbol, 'Return (%)']
            port = investment.loc[symbol, 'Portfolio (%)'] / 100

            m2 += ret * port

        print(m1, m2)

def calculate_shares(symbol: str, weight: float, currency: str):
    total_equity = qbot.get_usd_total_equity()
    amount = total_equity * weight
    curr_price = get_daily_prices(symbol)
    return (amount, math.floor(amount / curr_price))

if __name__ == '__main__':

    q = qbot(credentials.QUESTRADE_ACCOUNT_NUM)
    print(q.get_investment_summary())
    print(q.calculate_portfolio_return())