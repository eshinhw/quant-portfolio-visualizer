import os
import price
import smtplib
import pandas as pd
from fmp_db import fmp
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

def sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, subject, contents):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(contents)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


db = fmp()
df = db.load_financials()
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


mom_data = {
    'symbol': [],
    '52W_high': [],
    'currentPrice': [],
    '15%_discount': [],
    '25%_discount': [],
    '40%_discount': [],
    '90D_support': [],
    '180D_support': [],
    '360D_support': []
}

count = 0

for symbol in list(df_final['symbol']):
    count += 1
    print(f"{symbol} \t {count} / {len(list(df_final['symbol']))}")
    currPrice = db.get_current_price(symbol)
    high = price.calculate_prev_max_high(symbol, 260)
    d1 = high * 0.85
    d2 = high * 0.75
    d3 = high * 0.60

    m3 = price.calculate_prev_min_low(symbol, 90)
    m6 = price.calculate_prev_min_low(symbol, 180)
    m12 = price.calculate_prev_min_low(symbol, 360)

    msg = ""

    if currPrice > high:
        increase = (currPrice - high)/high * 100
        msg = f"{symbol}: New High {increase}"
        print(f"{symbol}: New High {increase}")
        sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, symbol, msg)
        continue
    if currPrice < m3:
        print(f'{symbol} \t 90D_support')
        msg += symbol + " 90D_Support /"
    if currPrice < m6:
        print(f'{symbol} \t 180D_support')
        msg += " 180D_Support /"
    if currPrice < m12:
        print(f'{symbol} \t 360D_support')
        msg += " 360D_Support /"
    if currPrice < d1:
        print(f'{symbol} \t 15%_Discount')
        msg += " 15%_Discount /"
    if currPrice < d2:
        print(f'{symbol} \t 25%_Discount')
        msg += " 25%_Discount /"
    if currPrice < d3:
        print(f'{symbol} \t 40%_Discount')
        msg += " 40%_Discount /"

    if msg != "":
        print(msg)
        sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, symbol, msg)

    mom_data['symbol'].append(symbol)
    mom_data['currentPrice'].append(currPrice)
    mom_data['52W_high'].append(high)
    mom_data['15%_discount'].append(d1)
    mom_data['25%_discount'].append(d2)
    mom_data['40%_discount'].append(d3)
    mom_data['90D_support'].append(m3)
    mom_data['180D_support'].append(m6)
    mom_data['360D_support'].append(m12)

mom_df = pd.DataFrame(mom_data)
mom_df.set_index('symbol', inplace=True)


