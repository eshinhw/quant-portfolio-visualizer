import os
import price
import smtplib
import credentials
import pandas as pd
import datetime as dt
from fmp_db import fmp
from email.message import EmailMessage

EMAIL_ADDRESS = credentials.GMAIL_ADDRESS
EMAIL_PASSWORD = credentials.GMAIL_PW

def sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    # msg.set_content("hello?")

    msg.add_alternative(f"""\

        <!DOCTYPE html>
        <html>
            <body>
                <h1>Watchlist Update</h1>
                {contents}
            </body>
        </html>
    """, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


db = fmp()
df = db.load_financials()
print(df)
df['marketCap'] = df['marketCap']/100000000

# ## Minimum Fundamental Ratio Requirements

minMktCap = 10
minRevGrowth = 0.5
minGPMargin = 0.2
minEPSGrowth = 0.1
minROE = 0.2
minDPSGrowth = 0.1
minDivYield = 0.02


df = df[df['marketCap'] > minMktCap]
conditions = (df['revenue_per_share_fiveY_growth'] > minRevGrowth) & (df['gross_profit_margin'] > minGPMargin) & (df['eps_growth'] > minEPSGrowth) & (df['roe'] > minROE)
df = df[conditions]
div_conds = (df['dps_fiveY_growth'] > minDPSGrowth) & (df['div_yield'] > minDivYield)
df_final = df[div_conds]

df_final.set_index('symbol', inplace=True)

print(df_final)


price_data = {
    'Symbol': [],
    'Name': [],
    'Exchange': [],
    'Sector': [],
    'Industry': [],
    '52W High': [],
    'Current Price': [],
    'Change (%)': [],
    'Dividend Yield': []
}

count = 0
email_contents = ""
for symbol in list(df_final.index):
    count += 1
    print(f"{symbol} \t {count} / {len(list(df_final.index))}")
    currPrice = round(db.get_current_price(symbol),2)
    high = round(price.calculate_prev_max_high(symbol, 260),2)
    name = df_final.loc[symbol, 'name']
    exchange = df_final.loc[symbol, 'exchange']
    sector = df_final.loc[symbol, 'sector']
    industry = df_final.loc[symbol, 'industry']
    div_yield = df_final.loc[symbol, 'div_yield']

    if currPrice < high:
        discount = (currPrice - high)/high * 100
        if discount < -10:
            price_data['Symbol'].append(symbol)
            price_data['Name'].append(name)
            price_data['Exchange'].append(exchange)
            price_data['Sector'].append(sector)
            price_data['Industry'].append(industry)
            price_data['52W High'].append(high)
            price_data['Current Price'].append(currPrice)
            price_data['Change (%)'].append(discount)
            price_data['Dividend Yield'].append(div_yield)

mom_df = pd.DataFrame(price_data)
mom_df.set_index('Symbol', inplace=True)
mom_df.sort_values(by='Dividend Yield', ascending=False, inplace=True)

today = str(dt.datetime.today().strftime('%Y-%b-%d'))

sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, f"Daily Stock Update ({today})", mom_df.to_html())




