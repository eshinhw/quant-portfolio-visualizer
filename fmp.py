import os
import json
import secret
import pprint
import requests
import mysql.connector


FMP_API_KEY = secret.FMP_API_KEYS
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
        self.mycursor.execute("USE fmp")

    def sp500_symbol_list(self):

        if os.path.exists('./sp500_symbols.json'):
            fp = open("./sp500_symbols.json", "r")
            data = json.load(fp)
            print(len(data['symbols']))
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

    def company_profile(self, symbol: str):

        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS company_profile (\
        id INT AUTO_INCREMENT PRIMARY KEY, \
        name VARCHAR(255), \
        symbol VARCHAR(20), \
        exchange VARCHAR(255), \
        sector VARCHAR(255), \
        industry VARCHAR(255), \
        marketCap int)""")

        data = requests.get(f"https://financialmodelingprep.com/api/v3/profile/{symbol.upper()}?apikey={FMP_API_KEY}").json()[0]
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

        data = requests.get(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={FMP_API_KEY}").json()[0]
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

        val = (
            symbol,
            float(div_yield),
            float(curr_ratio),
            float(div_per_share),
            float(gross_profit_margin),
            float(per),
            float(roe))

        self.mycursor.execute(sql,val)
        self.mydb.commit()

    def growth(self, symbol: str):

        data = requests.get(f"https://financialmodelingprep.com/api/v3/financial-growth/{symbol.upper()}?period=quarter&limit=20&apikey={FMP_API_KEY}").json()[0]

        pprint.pprint(data)
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS growth (\
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(255),
            date VARCHAR(255),
            gross_profit_margin float,
            eps_growth float,
            fcf_growth float,
            dps_fiveY_growth float,
            netIncome_per_share_fiveY_growth float,
            revenue_per_share_fiveY_growth float)""")

        sql = """
        INSERT INTO growth \
        (symbol, date, gross_profit_margin, eps_growth, fcf_growth, dps_fiveY_growth, netIncome_per_share_fiveY_growth, revenue_per_share_fiveY_growth) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        date = data['date']
        gross_profit_margin = data['grossProfitGrowth']
        eps_growth = data['epsgrowth']
        fcf_growth = data['freeCashFlowGrowth']
        dps_fiveY_growth = data['fiveYDividendperShareGrowthPerShare']
        netIncome_per_share_fiveY_growth = data['fiveYNetIncomeGrowthPerShare']
        revenue_per_share_fiveY_growth = data['fiveYRevenueGrowthPerShare']

        val = (symbol, date, float(gross_profit_margin), float(eps_growth), float(fcf_growth), float(dps_fiveY_growth), float(netIncome_per_share_fiveY_growth), float(revenue_per_share_fiveY_growth))

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
            self.mydb.commit()


# mycursor.execute("ALTER TABLE company_profile ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

# mycursor.execute("ALTER TABLE company_profile ADD COLUMN numEmployees INT")

# mycursor.execute("ALTER TABLE company_profile MODIFY COLUMN marketCap float")





if __name__ == '__main__':

    myfmp = fmp()

    myfmp.drop_all_databases()

    myfmp = fmp()

    symbols = myfmp.sp500_symbol_list()

    for symbol in symbols:



