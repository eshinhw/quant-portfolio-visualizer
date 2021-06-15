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
    msg.set_content(contents)

    msg.add_alternative("""\
        <!DOCTYPE html>
        <html>
            <body>
                {0}
            </body>
        </html>
    """.format(contents), subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


db = fmp()
df = db.load_financials()
print(df)
df['marketCap'] = df['marketCap']/100000000

# ## Minimum Fundamental Ratio Requirements

minMktCap = 1000
minRevGrowth = 0.3
minGPMargin = 0.2
minEPSGrowth = 0.1
minROE = 0.2
minDPSGrowth = 0.1
minDivYield = 0


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
    '52W High': [],
    'Current Price': [],
    'Change (%)': []
}

count = 0
email_contents = ""
for symbol in list(df_final['symbol']):
    count += 1
    print(f"{symbol} \t {count} / {len(list(df_final['symbol']))}")
    currPrice = round(db.get_current_price(symbol),2)
    high = round(price.calculate_prev_max_high(symbol, 260),2)
    name = df_final.loc[symbol, 'name']
    exchange = df_final.loc[symbol, 'exchange']
    sector = df_final.loc[symbol, 'sector']
    industry = df_final.loc[symbol, 'industry']

    if currPrice < high:
        discount = (currPrice - high)/high * 100
        if discount < -15:
            price_data['Symbol'].append(symbol)
            price_data['52W High'].append(high)
            price_data['Current Price'].append(currPrice)
            price_data['Change (%)'].append(discount)

mom_df = pd.DataFrame(price_data)
mom_df.set_index('Symbol', inplace=True)

today = dt.datetime.today()

sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, "Daily Stock Update " + str(today), mom_df.to_html())




