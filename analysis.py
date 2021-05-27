import pandas as pd
from fmp import fmp


db = fmp()

df = db.load_financials()

print(df)

