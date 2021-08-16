import pandas as pd

df = pd.read_csv('./R/data/dow_financials.csv')

dividendStocks = df.dropna()

print(dividendStocks)