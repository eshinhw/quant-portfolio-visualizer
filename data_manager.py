from fmp_db import fmp

# update table in database

# create table if table doesn't exist

# occassionally, update s&p500 symbols and dividend paying stocks

myfmp = fmp()

count = 0
# print(myfmp.table_exists('financials'))
if myfmp.table_exists('financials'):
    # update
    symbols = myfmp.get_symbols_from_db()
    for symbol in symbols:
        count += 1
        print(f"{symbol} {count}/{len(symbols)}")
        myfmp.update_financials(symbol)
        print("table update completed!")

else:
    # create and insert initial data
    symbols = myfmp.load_sp500_symbol_list()
    for symbol in symbols:
        count += 1
        print(f"{symbol} {count}/{len(symbols)}")
        myfmp.create_financials(symbol)
        print("table created successfully")
