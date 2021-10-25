import os
import json
import urllib
import pprint
import datetime as dt
import configparser
import pandas as pd
from questradeAPI.auth import Auth
from datetime import datetime, timedelta

CONFIG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'questrade.cfg')

class Questrade:
    def __init__(self, user_id, **kwargs):
        if 'config' in kwargs:
            self.config = self.__read_config(kwargs['config'])
        else:
            self.config = self.__read_config(CONFIG_PATH)

        auth_kwargs = {x: y for x, y in kwargs.items() if x in
                       ['token_path', 'refresh_token']}

        print(auth_kwargs)

        self.auth = Auth(user_id, **auth_kwargs, config=self.config)

    def __read_config(self, fpath):
        config = configparser.ConfigParser()
        with open(os.path.expanduser(fpath)) as f:
            config.read_file(f)
        return config

    @property
    def __base_url(self):
        return self.auth.token['api_server'] + self.config['Settings']['Version']

    def __build_get_req(self, url, params):
        if params:
            print('params')
            print(params)
            url = self.__base_url + url + '?' + urllib.parse.urlencode(params)
            print(url)
            # url = self.__base_url + url + '?' + 'startTime=2011-02-01T00:00:00-05:00&endTime=2011-02-28T00:00:00-05:00&'
            # url = self.__base_url + url + '?' + 'startTime=2011-02-01T00:00:00-05:00&endTime=2011-02-28T00:00:00-05:00&'
            # print(url)
            return urllib.request.Request(url)
        else:
            return urllib.request.Request(self.__base_url + url)

    def __get(self, url, params=None):
        req = self.__build_get_req(url, params)
        req.add_header(
            'Authorization',
            self.auth.token['token_type'] + ' ' +
            self.auth.token['access_token']
        )
        try:
            r = urllib.request.urlopen(req)
            return json.loads(r.read())
            # return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return json.loads(e.read())
            # return json.loads(e.read().decode('utf-8'))

    def __build_post_req(self, url, params):
        url = self.__base_url + url
        return urllib.request.Request(url, data=json.dumps(params).encode('utf8'))

    def __post(self, url, params):
        req = self.__build_post_req(url, params)
        req.add_header(
            'Authorization',
            self.auth.token['token_type'] + ' ' +
            self.auth.token['access_token']
        )
        try:
            r = urllib.request.urlopen(req)
            return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return json.loads(e.read().decode('utf-8'))

    @property
    def __now(self):
        return datetime.now().astimezone().strftime("%Y-%m-%d")

    def __days_ago(self, d):
        return (datetime.now().astimezone() - timedelta(days=d)).strftime("%Y-%m-%d")

    @property
    def time(self):
        return self.__get(self.config['API']['time'])

    @property
    def accounts(self):
        resp = self.__get(self.config['API']['Accounts'])
        account_ids = []
        for id in resp['accounts']:
            account_ids.append(id['number'])
        return account_ids

    def account_positions(self, id):
        positions = self.__get(self.config['API']['AccountPositions'].format(id))
        position_data = {
            'Symbol': [],
            'Description': [],
            'Currency': [],
            'Quantities': [],
            'Market Value': [],
            'Return (%)': [],
            'Portfolio (%)': []
        }
        total_market_value = self.get_usd_total_mv(id)
        total_costs = 0
        pprint.pprint(positions)
        for position in positions['positions']:
            # handle daily execution for closeQuantity
            if position['openQuantity'] != 0:
                symbol = position['symbol']
                description = self.symbols_search(prefix=symbol)['symbols'][0]['description']
                qty = position['openQuantity']
                cmv = position['currentMarketValue']
                currency = self.symbols_search(prefix=symbol)['symbols'][0]['currency']
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

    def account_balances(self, id):
        bal = self.__get(self.config['API']['AccountBalances'].format(id))

        data = {'Currency': [],
                'Cash': [],
                'Market_Value': [],
                'Total_Equity': [], 'Cash (%)': [], 'Investment (%)': []}

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

    def get_usd_total_equity(self, id):
        balance = self.account_balances(id)
        return balance.loc['USD','Total_Equity']

    def get_usd_total_mv(self, id):
        balance = self.account_balances(id)
        return balance.loc['USD', 'Market_Value']

    def get_cad_total_equity(self, id):
        balance = self.account_balances(id)
        return balance.loc['CAD','Total_Equity']

    def get_cad_total_mv(self, id):
        balance = self.account_balances(id)
        return balance.loc['CAD', 'Market_Value']

    def get_usd_total_cost(self, acctNum):
        positions = self.account_positions(acctNum)
        total_cost = 0
        for pos in positions:
            curr_cost = pos['totalCost']
            total_cost += curr_cost
        return total_cost


    def account_activities(self, id, **kwargs):
        print("account_activities input: ")
        print(kwargs)
        if 'startTime' not in kwargs:
            print('1')
            kwargs['startTime'] = self.__days_ago(1)
            kwargs['startTime'] = kwargs['startTime'] + "T00:00:00-05:00"
        if 'endTime' not in kwargs:
            print('2')
            kwargs['endTime'] = self.__now
            kwargs['endTime'] = kwargs['endTime'] + "T00:00:00-05:00"
        print("account_activities kwargs after update: ")
        print(kwargs)
        return self.__get(self.config['API']['AccountActivities'].format(id), kwargs)

    def symbol(self, id):
        return self.__get(self.config['API']['Symbol'].format(id))

    def symbols(self, **kwargs):
        if 'ids' in kwargs:
            kwargs['ids'] = kwargs['ids'].replace(' ', '')
        return self.__get(self.config['API']['Symbols'].format(id), kwargs)

    def symbols_search(self, **kwargs):
        return self.__get(self.config['API']['SymbolsSearch'].format(id), kwargs)

    def account_executions(self, id, **kwargs):
        return self.__get(self.config['API']['AccountExecutions'].format(id), kwargs)

    def account_orders(self, id, **kwargs):
        if 'ids' in kwargs:
            kwargs['ids'] = kwargs['ids'].replace(' ', '')
        return self.__get(self.config['API']['AccountOrders'].format(id), kwargs)

    def account_order(self, id, order_id):
        return self.__get(self.config['API']['AccountOrder'].format(id, order_id))

    def symbol_options(self, id):
        return self.__get(self.config['API']['SymbolOptions'].format(id))

    @property
    def markets(self):
        return self.__get(self.config['API']['Markets'])

    def markets_quote(self, id):
        return self.__get(self.config['API']['MarketsQuote'].format(id))

    def markets_quotes(self, **kwargs):
        if 'ids' in kwargs:
            kwargs['ids'] = kwargs['ids'].replace(' ', '')
        return self.__get(self.config['API']['MarketsQuotes'], kwargs)

    def markets_options(self, **kwargs):
        return self.__post(self.config['API']['MarketsOptions'], kwargs)

    def markets_strategies(self, **kwargs):
        return self.__post(self.config['API']['MarketsStrategies'], kwargs)

    def markets_candles(self, id, **kwargs):
        if 'startTime' not in kwargs:
            kwargs['startTime'] = self.__days_ago(1)
        if 'endTime' not in kwargs:
            kwargs['endTime'] = self.__now
        return self.__get(self.config['API']['MarketsCandles'].format(id), kwargs)

    def dividends(self, acctNum):
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
            activities = self.account_activities(acctNum, start, end)
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

    def portfolio_return(self, acctNum):
        total_mv = self.get_usd_total_mv(acctNum)
        total_cost = self.get_usd_total_cost(acctNum)
        m1 = round(100 * (total_mv - total_cost) / total_cost, 2)

        investment = self.account_positions(acctNum)

        m2 = 0
        for symbol in investment.index:

            ret = investment.loc[symbol, 'Return (%)']
            port = investment.loc[symbol, 'Portfolio (%)'] / 100

            m2 += ret * port

        print(m1, m2)

if __name__ == '__main__':
    q = Questrade('eshinhw')
    ids = q.accounts
    print(ids)
    # print(q.account_balances(ids[0]))
    # print(q.symbol(34659))
    # print(q.symbols_search(prefix='RY.TO'))

    # print(q.get_investment_summary(ids[0]))


    # print(q.dividends(ids[0]))
    # print(q.account_positions(ids[0]))
    print(q.account_activities(ids[0], startTime='2020-11-01T00:00:00-0'))