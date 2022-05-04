import yfinance as yf    
from datetime import datetime
    
df = yf.download("IBM", start= datetime(2018,1,1), end = datetime(2022,5,1),interval='1mo')
print(df.dropna())