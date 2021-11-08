import os
import pandas as pd

class OandaInstrument():

    def fx_instruments(self):
        quote = ['_USD','_CAD', '_JPY', '_CHF', '_SGD']
        major = ['AUD_', 'USD_', 'NZD_', 'CAD_', 'EUR_', 'GBP_', 'SGD_']
        quote_pairs = []
        major_pairs = []
        if os.name == "nt":
            df = pd.read_csv('./instruments.csv')
        if os.name == "posix":
            df = pd.read_csv('/home/eshinhw/pyTrader/instruments.csv')

        df['Instrument'] = df['Instrument'].str.replace('/','_')
        low_spread = df[df['Spread'] < 10].sort_values(by='Spread')

        for inst in low_spread['Instrument'].tolist():
            for q in quote:
                if q in inst:
                    quote_pairs.append(inst)

        for pair in quote_pairs:
            for m in major:
                if m in pair:
                    major_pairs.append(pair)
        return major_pairs

    def create_decimal_table(self):
        trading_instruments = self.fx_instruments()
        table = {}
        for inst in trading_instruments:
            if '_USD' in inst or '_CAD' in inst or '_CHF' in inst or '_SGD' in inst:
                table[inst] = {}
                table[inst]['decimal'] = 4
                table[inst]['multiple'] = 10 ** 4
            if '_JPY' in inst:
                table[inst] = {}
                table[inst]['decimal'] = 2
                table[inst]['multiple'] = 10 ** 2
        return table