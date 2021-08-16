import credentials
import pandas as pd
import datetime as dt
from fmpDB import fmp
from questrade import qbot
from utilities import calculate_prev_max_high, sendEmail

print(f"{dt.datetime.now()}: Beginning of Run File")

qt = qbot(credentials.QUESTRADE_ACCOUNT_NUM)

db = fmp()
df = db.load_financials()

# Minimum Fundamental Ratio Requirements
# Filtering Conditions

filters = {'Market Cap': 1,
           'Revenue Growth': 0.3,
           'Gross Profit Margin': 0.2,
           'EPS Growth': 0.15,
           'ROE': 0.2,
           '5 Years Average DPS Growth': 0.1,
           'Dividend Yield': 0.02
           }

conditions = (df['marketCap'] > filters['Market Cap']) & \
            (df['revenue_per_share_fiveY_growth'] > filters['Revenue Growth']) & \
            (df['gross_profit_margin'] > filters['Gross Profit Margin'])& \
            (df['eps_growth'] > filters['EPS Growth'])& \
            (df['roe'] > filters['ROE']) & \
            (df['dps_fiveY_growth'] > filters['5 Years Average DPS Growth']) & \
            (df['div_yield'] > filters['Dividend Yield'])

df = df[conditions]
df.set_index('symbol', inplace=True)

price_data = {
    'Symbol': [],
    'Name': [],
    'Exchange': [],
    'Sector': [],
    'Industry': [],
    'Dividend Yield': [],
    '52W High': [],
    'Current Price': [],
    'Change (%)': []
}

discount_pct = -10

count = 0

for symbol in list(df.index):
    count += 1
    print(f"{symbol} \t {count} / {len(list(df.index))}")
    currPrice = round(db.get_current_price(symbol),2)
    high = round(calculate_prev_max_high(symbol, 260),2)
    name = df.loc[symbol, 'name']
    exchange = df.loc[symbol, 'exchange']
    sector = df.loc[symbol, 'sector']
    industry = df.loc[symbol, 'industry']
    div_yield = df.loc[symbol, 'div_yield']

    if currPrice < high:
        discount = (currPrice - high)/high * 100
        if discount < discount_pct:
            price_data['Symbol'].append(symbol)
            price_data['Name'].append(name)
            price_data['Exchange'].append(exchange)
            price_data['Sector'].append(sector)
            price_data['Industry'].append(industry)
            price_data['Dividend Yield'].append(div_yield)
            price_data['52W High'].append(high)
            price_data['Current Price'].append(currPrice)
            price_data['Change (%)'].append(discount)

mom_df = pd.DataFrame(price_data)
mom_df.set_index('Symbol', inplace=True)
mom_df.index.name = None
mom_df.sort_values(by='Dividend Yield', ascending=False, inplace=True)

today = str(dt.datetime.today().strftime('%Y-%b-%d'))

filtersToEmail = ""

for key, val in filters.items():
    if key == 'Market Cap':
        filtersToEmail += f'&#9656; {key}: {val} Billion(s) <br>'
    else:
        filtersToEmail += f'&#9656; {key}: {val * 100} % <br>'

sendEmail(f"Daily Portfolio Update ({today})", curr_pos = qt.get_investment_summary().to_html(),filters=filtersToEmail, watchlist = mom_df.to_html())

print(f"{dt.datetime.now()}: End of Run File")



