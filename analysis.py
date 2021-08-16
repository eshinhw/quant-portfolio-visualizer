import pandas as pd

df = pd.read_csv('./R/data/dow_financials.csv')

df = df.dropna()

conditions = (df['Revenue_Growth'] > 0) & \
            (df['GPMargin'] > 0)& \
            (df['EPS_Growth'] > 0)& \
            (df['ROE'] > 0) & \
            (df['DPS_Growth'] > 0) & \
            (df['DivYield'] > 0)


df = df[conditions]