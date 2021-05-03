import momentum
import pandas as pd
from pytickersymbols import PyTickerSymbols
# https://pypi.org/project/pytickersymbols/

# Available Exchanges
# ['OMX Stockholm 30',
#  'SDAX',
#  'DOW JONES',
#  'OMX Helsinki 25',
#  'CAC 40',
#  'IBEX 35',
#  'FTSE 100',
#  'TECDAX',
#  'NASDAQ 100',
#  'Switzerland 20',
#  'MOEX',
#  'S&P 500',
#  'CAC Mid 60',
#  'DAX',
#  'BEL 20',
#  'AEX',
#  'MDAX',
#  'S&P 100',
#  'EURO STOXX 50']

pyticker = PyTickerSymbols()

def get_stocks_by_index(exchange: str):
    try:
        return list(pyticker.get_stocks_by_index(exchange))
    except:
        return "EXCHANGE NOT AVAILABLE"

def get_symbols_by_index(exchange: str):
    symbols = []
    try:
        for stock in get_stocks_by_index(exchange):
            symbols.append(stock['symbol'])
        return symbols
    except:
        return "EXCHANGE NOT AVAILABLE"

def get_sector_df():
    url = 'https://etfdb.com/etfs/sector/'
    df = pd.read_html(url)[0].drop([11], axis=0)

    sectors = list(df['Sector'])
    sectors = [x.lower() for x in sectors]
    sectors = [x.replace(' ', '-') for x in sectors]
    sectors = [x.replace('discretionary', 'discretionaries') for x in sectors]

    top_etfs = {}
    for s in sectors:
        sector_url = url + s + '/'
        sector_data = pd.read_html(sector_url)[0]
        etf_symbol = sector_data.loc[0, 'Symbol']
        etf_name = sector_data.loc[0, 'ETF Name']
        etf_industry = sector_data.loc[0, 'Industry']
        etf_aum = sector_data.loc[0, 'Total Assets ($MM)']
        top_etfs[s] = {}
        top_etfs[s]['symbol'] = etf_symbol
        top_etfs[s]['name'] = etf_name
        top_etfs[s]['industry'] = etf_industry
        top_etfs[s]['aum'] = etf_aum

    sector_data = {
        'Symbol': [],
        'Sector': [],
        'Industry': [],
        'AUM': []
    }

    for etf in top_etfs.keys():
        symbol = top_etfs[etf]['symbol']
        sector = etf
        industry = top_etfs[etf]['industry']
        aum = top_etfs[etf]['aum']

        sector_data['Symbol'].append(symbol)
        sector_data['Sector'].append(sector)
        sector_data['Industry'].append(industry)
        sector_data['AUM'].append(aum)

    sector_df = pd.DataFrame(sector_data)
    sector_df.set_index('Symbol', inplace=True)

    return sector_df

if __name__ == '__main__':

    sector_df = get_sector_df()
    print(list(sector_df.index))

    for x in list(sector_df.index):
        sector_df.loc[x,'Momentum'] = momentum.calculate_equal_weight_momentum(x, [1,3,6,12])

    print(sector_df)
    # sector_momentum = momentum.calculate_equal_weight_momentum(sector_etfs, start_date, end_date, [1,3,6,12])

    # sector_df = pd.DataFrame(sector_data)
    # sector_df.set_index('Symbol', inplace=True)
    # sector_df['EW_MOMENTUM'] = sector_momentum['EW_MOMENTUM']
    # sector_df.sort_values(by='EW_MOMENTUM', ascending=False)