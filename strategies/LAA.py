import pandas as pd
from strategies.VAA import VAA
import yfinance as yf


def decision():
    vaa = VAA()
    vaa_df = vaa.decision()
    if "QQQ" in vaa_df.columns:
        allocate = {'Asset': ['IWD', 'IEF', 'GLD', 'QQQ'], 'Weights (%)': [
            25, 25, 25, 25]}
        laa_df = pd.DataFrame(allocate)
        laa_df.set_index('Asset', inplace=True)
        return laa_df
    else:
        allocate = {'Asset': ['IWD', 'IEF', 'GLD', 'SHY'],
                    'Description': [], 'Weights (%)': [25, 25, 25, 25]}
        count = 0
        for asset in allocate['Asset']:
            count += 1
            print(f"{count} / {len(allocate['Asset'])}")
            desc = yf.Ticker(asset).info['longName']
            allocate['Description'].append(desc)
        laa_df = pd.DataFrame(allocate)
        laa_df.set_index('Asset', inplace=True)
        return laa_df
