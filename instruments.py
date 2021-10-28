import pandas as pd
from oanda import Oanda
import demo_credentials

df = pd.read_csv('./instruments.csv')

df['Instrument'] = df['Instrument'].str.replace('/','_')

print(df)

# print(type(df[0,'Spread']))
# inst = df[df['Spread'] < 10]
# print(inst)


o = Oanda(demo_credentials.OANDA_API_KEY, demo_credentials.VOL_BREAKOUT_ACCOUNT_ID)

print(o.get_ohlc('WHEAT_USD', 30, 'D'))
