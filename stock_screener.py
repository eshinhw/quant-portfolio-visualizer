import yfinance as yf
import pandas as pd

symbol = 'AAPL'



sData = yf.Ticker(symbol)

print(sData.info) 

# df = sData.recommendations()

# cal = sData.calendar()