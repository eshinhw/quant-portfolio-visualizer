import pandas as pd
import utilities
from dataSrc import sp500_symbols, dow_symbols, financials

# df = pd.read_csv('./R/data/dow_financials.csv')

# sp500 = sp500_symbols()
dowTickers = dow_symbols()

df = financials(dowTickers)

df = df.dropna()

conditions = (df['Revenue_Growth'] > 0) & \
            (df['GPMargin'] > 0)& \
            (df['EPS_Growth'] > 0)& \
            (df['ROE'] > 0) & \
            (df['DPS_Growth'] > 0) & \
            (df['DivYield'] > 0)
df = df[conditions]

# Compute historical momentum
# Average momentum of prev 6M, 12M and 24M

mom_list = []
for symbol in df['symbol']:
    print(symbol)
    m6_momentum = utilities.calculate_hist_momentum(symbol, 120)
    m12_momentum = utilities.calculate_hist_momentum(symbol, 252)
    m24_momentum = utilities.calculate_hist_momentum(symbol, 504)
    avg_momentum = (m6_momentum + m12_momentum + m24_momentum) / 3
    mom_list.append(avg_momentum)

df['momentum'] = mom_list
print(df)

df['mom_rank'] = df['momentum'].rank()

print(df)

