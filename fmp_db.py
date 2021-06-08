import os
import json
import pprint
import requests
import credentials
import pandas as pd
import mysql.connector
from typing import List
from sqlalchemy import create_engine
from price import calculate_momentum
from pandas.core.frame import DataFrame

FMP_API_KEY = credentials.FMP_API_KEYS
MOMENTUMS = [3,6,12,36,60]

class fmp:
    def __init__(self) -> None:
        try:
            self.mydb = mysql.connector.connect(
                host=credentials.DB_HOST,
                user=credentials.DB_USER,
                password=credentials.DB_PASSWORD
            )
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("CREATE DATABASE IF NOT EXISTS fmp")
            self.mycursor.execute("USE fmp")
        except Exception as e:
            print(e)

    def load_sp500_symbol_list(self) -> List[str]:

        if os.path.exists('./sp500_symbols.json'):
            fp = open("./sp500_symbols.json", "r")
            data = json.load(fp)
            return data['symbols']

        out_dict = {}
        symbols = []
        sp500 = requests.get(f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={FMP_API_KEY}").json()
        for data in sp500:
            symbols.append(data['symbol'])

        out_dict['symbols'] = symbols

        with open('./sp500_symbols.json', 'w') as fp:
            json.dump(out_dict, fp)

        return symbols

    def get_symbols_from_db(self):
        self.mycursor.execute('SELECT symbol from financials')
        res = self.mycursor.fetchall()
        symbols = [data[0] for data in res]
        return symbols

    def get_current_price(self, symbol: str):
        price = requests.get(f"https://financialmodelingprep.com/api/v3/quote-short/{symbol.upper()}?apikey={FMP_API_KEY}").json()
        return price[0]['price']

    def table_exists(self, table_name: str):
        self.mycursor.execute("SHOW TABLES")
        result = self.mycursor.fetchall()
        for tb in result:
            if table_name in tb:
                return 1
        return 0

    def create_financials(self, symbol: str) -> None:
        symbol = symbol.upper()
        self.mycursor.execute("""
            CREATE TABLE IF NOT EXISTS financials (
                symbol VARCHAR(20) PRIMARY KEY,
                name VARCHAR(255),
                exchange VARCHAR(255),
                sector VARCHAR(255),
                industry VARCHAR(255),
                marketCap float,
                numEmployees int,
                revenue_per_share_fiveY_growth float,
                gross_profit_margin float,
                roe float,
                eps_growth float,
                div_yield float,
                div_per_share float,
                dps_fiveY_growth float
            )""")
        try:
            ratio_ttm = requests.get(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={FMP_API_KEY}").json()[0]
        except:
            return

        div_yield = ratio_ttm['dividendYieldTTM']
        if not div_yield: div_yield = -1
        div_per_share = ratio_ttm['dividendPerShareTTM']
        if not div_per_share: div_per_share = -1
        gross_profit_margin = ratio_ttm['grossProfitMarginTTM']
        roe = ratio_ttm['returnOnEquityTTM']
        try:
            growth = requests.get(f"https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?period=quarter&limit=20&apikey={FMP_API_KEY}").json()[0]
        except:
            return

        eps_growth = growth['epsgrowth']
        dps_fiveY_growth = growth['fiveYDividendperShareGrowthPerShare']
        revenue_per_share_fiveY_growth = growth['fiveYRevenueGrowthPerShare']
        try:
            profile = requests.get(f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FMP_API_KEY}").json()[0]
        except:
            return

        name = profile['companyName']
        exchange = profile['exchangeShortName']
        sector = profile['sector']
        industry = profile['industry']
        marketCap = profile['mktCap']
        numEmployees = profile['fullTimeEmployees']

        sql = """
        INSERT IGNORE INTO financials (
            symbol,
            name,
            exchange,
            sector,
            industry,
            marketCap,
            numEmployees,
            revenue_per_share_fiveY_growth,
            gross_profit_margin,
            roe,
            eps_growth,
            div_yield,
            div_per_share,
            dps_fiveY_growth
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        val = (
            symbol,
            name,
            exchange,
            sector,
            industry,
            float(marketCap),
            int(numEmployees),
            float(revenue_per_share_fiveY_growth),
            float(gross_profit_margin),
            float(roe),
            float(eps_growth),
            float(div_yield),
            float(div_per_share),
            float(dps_fiveY_growth))

        self.mycursor.execute(sql,val)
        self.mydb.commit()

    def update_financials(self, symbol: str):
        symbol = symbol.upper()
        try:
            ratio_ttm = requests.get(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={FMP_API_KEY}").json()[0]
        except:
            return

        div_yield = ratio_ttm['dividendYieldTTM']
        div_per_share = ratio_ttm['dividendPerShareTTM']
        gross_profit_margin = ratio_ttm['grossProfitMarginTTM']
        roe = ratio_ttm['returnOnEquityTTM']
        try:
            growth = requests.get(f"https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?period=quarter&limit=20&apikey={FMP_API_KEY}").json()[0]
        except:
            return

        eps_growth = growth['epsgrowth']
        dps_fiveY_growth = growth['fiveYDividendperShareGrowthPerShare']
        revenue_per_share_fiveY_growth = growth['fiveYRevenueGrowthPerShare']
        try:
            profile = requests.get(f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FMP_API_KEY}").json()[0]
        except:
            return

        name = profile['companyName']
        exchange = profile['exchangeShortName']
        sector = profile['sector']
        industry = profile['industry']
        marketCap = profile['mktCap']
        numEmployees = profile['fullTimeEmployees']

        sql="""
            UPDATE financials
            SET
                name = %s,
                exchange = %s,
                sector = %s,
                industry = %s,
                marketCap = %s,
                numEmployees = %s,
                revenue_per_share_fiveY_growth = %s,
                gross_profit_margin = %s,
                roe = %s,
                eps_growth = %s,
                div_yield = %s,
                div_per_share = %s,
                dps_fiveY_growth = %s
            WHERE
                symbol = %s
            """
        val=(
            name,
            exchange,
            sector,
            industry,
            float(marketCap),
            int(numEmployees),
            float(revenue_per_share_fiveY_growth),
            float(gross_profit_margin),
            float(roe),
            float(eps_growth),
            float(div_yield),
            float(div_per_share),
            float(dps_fiveY_growth),
            symbol)

        self.mycursor.execute(sql,val)
        self.mydb.commit()

    # def create_momentum(self, symbol:str):
    #     symbol = symbol.upper()
    #     self.mycursor.execute("""
    #         CREATE TABLE IF NOT EXISTS momentum (
    #             symbol VARCHAR(20) PRIMARY KEY,
    #             1M float,
    #             3M float,
    #             6M float,
    #             1Y float,
    #             3Y float,
    #             5Y float,
    #             10Y float
    #         )""")

    #     sql = """
    #         INSERT IGNORE INTO momentum (
    #             symbol,
    #             1M,
    #             3M,
    #             6M,
    #             1Y,
    #             3Y,
    #             5Y,
    #             10Y
    #         )
    #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    #     val = tuple(calculate_momentum(symbol, MOMENTUMS))
    #     self.mycursor.execute(sql,val)
    #     self.mydb.commit()

    # def update_momentum(self, symbol: str):
    #     symbol = symbol.upper()

    #     sql = """
    #     UPDATE momentum
    #     SET
    #         symbol = %s,
    #         1M = %s,
    #         3M = %s,
    #         6M = %s,
    #         1Y = %s,
    #         3Y = %s,
    #         5Y = %s,
    #         10Y = %s
    #     WHERE
    #         symbol = %s
    #     """
    #     val = tuple(calculate_momentum(symbol, MOMENTUMS) + [symbol])
    #     self.mycursor.execute(sql,val)
    #     self.mydb.commit()

    def load_financials(self) -> DataFrame:
        dbcon = create_engine(f'mysql://{credentials.DB_USER}:{credentials.DB_PASSWORD}@{credentials.DB_HOST}/fmp').connect()
        df = pd.read_sql_table('financials', dbcon)
        return df

    # def load_momentum(self) -> DataFrame:
    #     dbcon = create_engine(f'mysql://{credentials.DB_USER}:{credentials.DB_PASSWORD}@{credentials.DB_HOST}/fmp').connect()
    #     df = pd.read_sql_table('momentum', dbcon)
    #     return df

    def add_column_into_dbtable(self, tb_name: str, val: str):
        self.mycursor.execute(f"ALTER TABLE {tb_name} ADD COLUMN {val}")

    def modify_column_type(self, tb_name: str, col_name: str, new_type: str):
        self.mycursor.execute(f"ALTER TABLE {tb_name} MODIFY COLUMN {col_name} {new_type}")


    def drop_all_databases(self) -> None:
        self.mycursor.execute("SHOW DATABASES")
        print(list(self.mycursor))
        excluded = ['sys', 'information_schema', 'performance_schema', 'mysql']
        db_names = []

        for name in self.mycursor:
            if name[0] not in excluded:
                db_names.append(name[0])

        for name in db_names:
            self.mycursor.execute(f"DROP DATABASE {name}")
            self.mydb.commit()


if __name__ == '__main__':

    myfmp = fmp()
    # symbols = myfmp.load_sp500_symbol_list()
    # count = 0
    # if myfmp.table_exists('financials'):
    #     # update
    #     for symbol in symbols:
    #         count += 1
    #         myfmp.update_financials(symbol)
    #         print(f"{count}/{len(symbols)}")
    # else:
    #     # create and insert initial data
    #     for symbol in symbols:
    #         count += 1
    #         myfmp.create_financials(symbol)
    #         print(f"{count}/{len(symbols)}")

    # myfmp.drop_all_databases()

    myfmp.get_symbols_from_db()






