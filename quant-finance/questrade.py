from __future__ import print_function, unicode_literals
from os import path, remove, system
import numpy as np
import pandas as pd
import datetime as dt
from qtrade import Questrade
import yfinance as yf
from PyInquirer import prompt, print_json


def new_access_code():
    ask_access_code = [
        {
            'type': 'password',
            'message': 'VALIDATION ERROR: Enter new valid access code from Questrade',
            'name': 'access_code'
        }
    ]
    new_access_code = prompt(ask_access_code).get('access_code')
    return new_access_code


class QuestradeBot:
    def __init__(self, acctNum):
        # Initialize Questrade Instance
        if path.exists("./access_token.yml"):
            #print("first try in questrade")
            self.qtrade = Questrade(token_yaml='./access_token.yml')
            try:
                acct_list = self.qtrade.get_account_id()
                #print(acctNum in acct_list)
                assert acctNum in acct_list
            except:
                #print("first if statement")
                self.qtrade.refresh_access_token(from_yaml=True)
                self.qtrade = Questrade(token_yaml='./access_token.yml')
                try:
                    assert acctNum in self.qtrade.get_account_id()
                except:
                    #print("yml file removed!")
                    remove("./access_token.yml")
                    # get new access code
                    access_code = new_access_code()
                    self.qtrade = Questrade(access_code=access_code)
        else:
            #print("no yml file exist")
            access_code = new_access_code()
            self.qtrade = Questrade(access_code=access_code)
            try:
                accts_list = self.qtrade.get_account_id()
            except:
                while not isinstance(accts_list, list):
                    #print("in while loop")
                    access_code = new_access_code()
                    self.qtrade = Questrade(access_code=access_code)

        self.acctNum = acctNum

    def get_acct_id(self):
        return self.qtrade.get_account_id()

    def get_ticker_info(self, symbol: str):
        return self.qtrade.ticker_information(symbol)

    def get_acct_positions(self):
        return self.qtrade.get_account_positions(self.acctNum)

    def _get_account_activities(self):
        return self.qtrade.get_account_activities(self.acctNum)

    def get_usd_total_equity(self):
        balance = self.get_account_balance_summary()
        return balance.loc['USD', 'Total_Equity']

    def get_usd_total_mv(self):
        balance = self.get_account_balance_summary()
        return balance.loc['USD', 'Market_Value']

    def get_cad_total_equity(self):
        balance = self.get_account_balance_summary()
        return balance.loc['CAD', 'Total_Equity']

    def get_cad_total_mv(self):
        balance = self.get_account_balance_summary()
        return balance.loc['CAD', 'Market_Value']

    def get_usd_total_cost(self):
        positions = self.get_acct_positions()
        total_cost = 0
        for pos in positions:
            curr_cost = pos['totalCost']
            total_cost += curr_cost
        return total_cost

    def get_account_balance_summary(self):
        bal = self.qtrade.get_account_balances(self.acctNum)

        data = {'Currency': [], 'Cash': [], 'Market_Value': [],
                'Total_Equity': [], 'Cash (%)': [], 'Investment (%)': []}

        for x in bal['perCurrencyBalances']:
            data['Currency'].append(x['currency'])
            data['Cash'].append(x['cash'])
            data['Market_Value'].append(x['marketValue'])
            data['Total_Equity'].append(x['totalEquity'])
            if x['totalEquity'] != 0:
                data['Cash (%)'].append(
                    round(100 * x['cash']/x['totalEquity'], 2))
                data['Investment (%)'].append(
                    round(100 * x['marketValue']/x['totalEquity'], 2))
            else:
                data['Cash (%)'].append(0)
                data['Investment (%)'].append(0)

        df = pd.DataFrame(data)
        df.set_index('Currency', inplace=True)
        #print(tabulate(df, headers='keys'))
        return df

    def get_investment_summary(self):
        # p&l
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
        positions = self.qtrade.get_account_positions(self.acctNum)
        for position in positions:
            # handle daily execution for closeQuantity
            if position['openQuantity'] != 0:
                symbol = position['symbol']
                description = self.qtrade.ticker_information(symbol)[
                    'description']
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
                position_data['Portfolio (%)'].append(
                    round(100 * (cmv / total_market_value), 2))

        portfolio = pd.DataFrame(position_data)
        portfolio.set_index('Symbol', inplace=True)
        #portfolio.index.name = None
        # print(tabulate(portfolio))
        return portfolio

    def get_historical_dividend_income(self, period):
        # identify the first date for creation
        endDate = dt.date.today().strftime("%Y-%m-%d")
        startDate = dt.date.today() - dt.timedelta(days=period)
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
            activities = self.qtrade.get_account_activities(
                self.acctNum, start, end)
            monthly_div = 0
            for activity in activities:
                if activity['type'] == 'Dividends':
                    monthly_div = monthly_div + activity['netAmount']
            output[dt.datetime.strptime(
                start, "%Y-%m-%d").strftime("%Y-%m")] = monthly_div
            total_div_earned = total_div_earned + monthly_div

        monthly_div_df = pd.DataFrame.from_dict(
            output, orient='index', columns=['Monthly_Dividend_Income'])

        return monthly_div_df

    def _monthly_return(self, assets):
        monthly_prices = pd.DataFrame()
        for asset in assets:
            monthly_prices[asset] = yf.download(asset, start=dt.datetime(
                2018, 1, 1), end=dt.datetime.today(), interval='1mo', progress=False)['Adj Close']

        monthly_returns = monthly_prices.pct_change()
        monthly_returns.dropna(inplace=True)

        return monthly_returns

    def _cumulative_returns(self, assets, weights):
        prices = pd.DataFrame()

        for symbol in assets:
            prices[symbol] = yf.download(symbol, start=dt.datetime(
                2018, 1, 1), end=dt.datetime.today(), interval='1mo', progress=False)['Adj Close']

        prices.dropna(inplace=True)
        monthly_returns = prices.pct_change()
        monthly_returns = monthly_returns.shift(-1)
        monthly_returns['port'] = monthly_returns.dot(weights)
        cum_returns = np.exp(np.log1p(monthly_returns['port']).cumsum())[:-1]
        return cum_returns

    def _cagr(self, assets, weights):
        cum_ret = self._cumulative_returns(assets, weights)
        first_value = cum_ret[0]
        last_value = cum_ret[-1]
        years = len(cum_ret.index)/12
        cagr = (last_value/first_value)**(1/years) - 1
        return cagr

    def _mdd(self, assets, weights):
        cum_ret = self._cumulative_returns(assets, weights)
        previous_peaks = cum_ret.cummax()
        drawdown = (cum_ret - previous_peaks) / previous_peaks
        port_mdd = drawdown.min()
        return port_mdd

    def calculate_portfolio_performance(self):

        BM_assets = ['SPY', 'IEF']
        BM_weights = np.array([0.6, 0.4])

        BM_cagr = round(self._cagr(BM_assets, BM_weights) * 100, 2)
        BM_mdd = round(self._mdd(BM_assets, BM_weights) * 100, 2)

        investments = self.get_investment_summary()

        port_assets = list(investments.index)
        port_weights = np.array(list(investments['Portfolio (%)'] / 100))
        port_cagr = round(self._cagr(port_assets, port_weights) * 100, 2)
        port_mdd = round(self._mdd(port_assets, port_weights) * 100, 2)

        stat = {'Portfolio': ['BenchMark', 'CurrentPortfolio'], 'CAGR (%)': [
            BM_cagr, port_cagr], 'MDD (%)': [BM_mdd, port_mdd]}

        stat_df = pd.DataFrame(stat)
        stat_df.set_index('Portfolio', inplace=True)

        return stat_df

    def strategy_allocation(self):
        # cash allocation
        # total equity - cash = allocatable amount
        total_equity = self.get_usd_total_equity()
        total_mv = self.get_usd_total_mv()
        curr_cash = total_equity - total_mv
        print(curr_cash)
        target_cash = total_equity * (self.cash_rate/100)

        if target_cash < curr_cash:
            # invest more from curr_cash
            invest_amount = curr_cash - target_cash
            print("invest more from curr_cash")

        else:
            # sell some from investment to increase curr_cash
            new_market_value = total_mv - (target_cash - curr_cash)
            print("sell some from investment to increase curr_cash")
