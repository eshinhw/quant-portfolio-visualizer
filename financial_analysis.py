import pandas as pd
from fmp import fmp


db = fmp()

df = db.load_financials()

df.set_index('symbol', inplace=True)
print(df)

# Qualifying Conditions


