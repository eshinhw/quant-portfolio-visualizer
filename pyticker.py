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

if __name__ == '__main__':

    sp = get_symbols_by_index('DOW JONES')
    print(sp)