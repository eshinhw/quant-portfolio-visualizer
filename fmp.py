import json
import secret
import pprint
import requests
import mysql.connector


API_KEY = secret.FMP_API_KEYS
DB_PW = secret.DB_PASSWORDD

class fmp:
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DB_PW
        )

        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS fmp")
        self.mycursor.execute(f"USE fmp")


    def company_profile(self, symbol: str):

        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS company_profile (\
        id INT AUTO_INCREMENT PRIMARY KEY, \
        name VARCHAR(255), \
        symbol VARCHAR(20), \
        exchange VARCHAR(255), \
        sector VARCHAR(255), \
        industry VARCHAR(255), \
        marketCap int)""")

        data = requests.get(f"https://financialmodelingprep.com/api/v3/profile/{symbol.upper()}?apikey={API_KEY}").json()[0]
        #pprint.pprint(data)

        name = data['companyName']
        symbol = data['symbol']
        exchange = data['exchangeShortName']
        sector = data['sector']
        industry = data['industry']
        marketCap = data['mktCap']
        numEmployees = data['fullTimeEmployees']

        sql = """
        INSERT INTO company_profile \
        (name, symbol, exchange, sector, industry, marketCap, numEmployees) \
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        val = (name, symbol, exchange, sector, industry, float(marketCap), int(numEmployees))

        self.mycursor.execute(sql,val)
        self.mydb.commit()

    def ratio_ttm(self, symbol: str):
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS ratio_ttm (\
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(255),
            div_yield float,
            curr_ratio float,
            div_per_share float,
            gross_profit_margin float,
            per float,
            roe float)""")

        data = requests.get(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={API_KEY}").json()[0]
        #pprint.pprint(data)

        div_yield = data['dividendYieldTTM']
        curr_ratio = data['currentRatioTTM']
        div_per_share = data['dividendPerShareTTM']
        gross_profit_margin = data['grossProfitMarginTTM']
        per = data['priceEarningsRatioTTM']
        roe = data['returnOnEquityTTM']

        sql = """
        INSERT INTO ratio_ttm \
        (symbol, div_yield, curr_ratio, div_per_share, gross_profit_margin, per, roe) \
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        val = (symbol, float(div_yield), float(curr_ratio), float(div_per_share), float(gross_profit_margin), float(per), float(roe))

        self.mycursor.execute(sql,val)
        self.mydb.commit()


    def drop_all_databases(self):

        self.mycursor.execute("SHOW DATABASES")
        excluded = ['sys', 'information_schema', 'performance_schema', 'mysql']
        db_names = []

        for name in self.mycursor:
            if name[0] not in excluded:
                db_names.append(name[0])

        for name in db_names:
            self.mycursor.execute(f"DROP DATABASE {name}")
            self.db.commit()


# def sql_add_column():


# mycursor.execute("ALTER TABLE company_profile ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

# mycursor.execute("ALTER TABLE company_profile ADD COLUMN numEmployees INT")

# mycursor.execute("ALTER TABLE company_profile MODIFY COLUMN marketCap float")





if __name__ == '__main__':

    myfmp = fmp()

    myfmp.ratio_ttm('AAPL')


