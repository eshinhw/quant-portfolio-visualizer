import os
import json
import requests
import sqlalchemy
import pandas as pd
import datetime as dt
import yfinance as yf
import mysql.connector
import pandas_datareader.data as web

with open('./credentials.txt', 'r') as fp:
    secret = fp.readlines()
    host_ip = secret[0].rstrip('\n')
    user_id = secret[1].rstrip('\n')
    pw = secret[2]
    fp.close()

# creds = {'usr': user_id,
#         'pwd': pw,
#         'hst': host_ip,
#         'prt': 3306,
#         'dbn': 'financial_data'}
# # MySQL conection string.
# connstr = 'mysql+mysqlconnector://{usr}:{pwd}@{hst}:{prt}/{dbn}'
# # Create sqlalchemy engine for MySQL connection.
# engine = sqlalchemy.create_engine(connstr.format(**creds))

# db = mysql.connector.connect(
#     host = host_ip,
#     user = user_id,
#     passwd = pw,
#     db = 'financial_data'
# )

# mycursor = db.cursor()

# https://financialmodelingprep.com/developer/docs

fmp_api = open("./fmp_api.txt", 'r').read()

class db_master:

    def __init__(self, symbol, key):
        self.key = key
        self.db = mysql.connector.connect(
            host = host_ip,
            user = user_id,
            passwd = pw
        )
        self.symbol = symbol.upper()
        print(self.symbol)
        self.mycursor = self.db.cursor()
        self.mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.symbol}")
        self.db.commit()

        creds = {'usr': user_id,
        'pwd': pw,
        'hst': host_ip,
        'prt': 3306,
        'dbn': self.symbol}
        connstr = 'mysql+mysqlconnector://{usr}:{pwd}@{hst}:{prt}/{dbn}'
        self.engine = sqlalchemy.create_engine(connstr.format(**creds))

    def income_statement(self, period: str, limit: int):
        if period.upper() == 'Y':
            annual = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{self.symbol}?limit={limit}&apikey={self.key}").json()
            return annual

            #annual = requests.get(f'https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={key}')
        if period.upper() == 'Q':
            quarter = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{self.symbol}?period=quarter&limit={limit}&apikey={self.key}").json()
            return quarter

        return None

    def financial_ratios(self, limit: int):
        self.mycursor.execute(f"USE {self.symbol}")
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS Financial_Ratios (Date VARCHAR(100) NOT NULL, Ratio VARCHAR(255) NOT NULL, Value float)")
        self.db.commit()

        # data = {'Symbol': [], 'Date': [], 'Revenue_Growth': [], 'ROE': [], 'Dividend_Yield': [], 'Payout Ratio': []}

        financial_growth = requests.get(f'https://financialmodelingprep.com/api/v3/financial-growth/{self.symbol}?period=quarter&limit={limit}&apikey={self.key}').json()[0]
        financial_ratios = requests.get(f'https://financialmodelingprep.com/api/v3/ratios-ttm/{self.symbol}?apikey={self.key}').json()[0]

        vals = []
        date = financial_growth.get('date')

        for k in financial_growth.keys():
            if k in ('symbol', 'period', 'date'):
                continue
            else:
                val = financial_growth.get(k)
                vals.append((date,k,val))

        for k in financial_ratios.keys():
            val = financial_ratios.get(k)
            vals.append((date,k,val))

        self.mycursor.executemany("INSERT INTO Financial_Ratios (Date, Ratio, Value) VALUES (%s,%s,%s)", vals)
        self.db.commit()

    def price_df_to_sql(self):
        try:
            prices = yf.Ticker(self.symbol).history(period='max')
        except:
            return None

        prices.reset_index(inplace=True)

        self.mycursor.execute(f"CREATE TABLE IF NOT EXISTS Price (Date datetime, Open float, High float, Low float, Close float, Dividends float, Stock_Splits float)")
        self.db.commit()

        prices.to_sql(name='Price', con=self.engine, if_exists='replace', index=False)

    def price_sql_to_df(self):
        self.mycursor.execute(f"SELECT * FROM Price")

        df = pd.DataFrame(self.mycursor.fetchall(), columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock_Splits'])
        df.set_index('Date',inplace=True)
        return df

if __name__ == '__main__':

    # if os.path.exists('./apple_data.json'):
    #     with open('./apple_data.json', 'r') as fp:
    #         x = json.load(fp)
    # else:
    #     aapl = db_master('AAPL', fmp_api)
    #     x = aapl.financial_ratios(5)
    #     with open('./apple_data.json', 'w') as fp:
    #         json.dump(x, fp)

    # x = x[0]
    # for k in x.keys():
    #     val = x.get(k)

    aapl = db_master('aapl', fmp_api)
    aapl.financial_ratios(20)
    aapl.price_df_to_sql()

    # abc = db_master('abc', fmp_api)

