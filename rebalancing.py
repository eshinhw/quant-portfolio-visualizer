import questrade as qt
import pandas as pd
from prettytable import PrettyTable

# input target allocation ratio bewteen two assets
target = {'VFV.TO': 0.8, 'XBB.TO': 0.2}
# input transaction cost for selling assets
transaction = 5

acctNum = qt.get_account_num()[0]

totalEquity = qt.get_active_balance_cad(acctNum)['totalEquity']
cash = qt.get_active_balance_cad(acctNum)['cash']

positions = qt.get_open_positions(acctNum)

df = pd.DataFrame()

# add positions into dataframe

for position in positions:    
    
    symbol = position['symbol']
    openQuantity = position['openQuantity']
    currMV = position['currentMarketValue']
    currPrice = position['currentPrice']    
    t = target[position['symbol']]
    
    df = df.append(position, ignore_index=True)    

df.set_index('symbol', inplace=True)

# calculate quantity changes for rebalancing

for symbol in df.index:
    
    df.loc[symbol,'targetValue'] = (totalEquity * target[symbol])
    df.loc[symbol,'variation'] = df.loc[symbol,'targetValue'] - df.loc[symbol,'currentMarketValue']  
    df.loc[symbol,'Qty Change'] = df.loc[symbol,'variation'] / df.loc[symbol,'currentPrice']
    
# change datatype for certain columns

df = df.astype({'Qty Change': int, 'symbolId': int, 'openQuantity': int})

# sort by qty change so that we can sell some first and buy other later with more cash

df.sort_values(by=['Qty Change'], inplace=True)

# iterate from the top to sell first and buy later with cash adjustment

x = PrettyTable()

x.field_names = ['SYMBOL', 'ACTION REQ.', '# SHARES', 'PRICE']

for symbol in df.index:

    qty = df.loc[symbol,'Qty Change']
    currP = df.loc[symbol, 'currentPrice']
    
    # buying
    if qty > 0:
        buy = qty * currP
        cash = cash - buy
        df.loc[symbol, 'after rebalancing'] = df.loc[symbol, 'currentMarketValue'] + buy
        x.add_row([symbol, 'BUY', int(qty), currP])
        #print("Total ${} is subtracted from cash account".format(buy))
    
    # selling
    elif qty < 0:
        sell = (-qty) * currP
        cash = cash + sell - transaction
        df.loc[symbol, 'after rebalancing'] = df.loc[symbol, 'currentMarketValue'] - sell
        x.add_row([symbol, 'SELL', -int(qty), currP])
        #print("Total ${} is added from cash account".format(sell))
    
    # no rebalancing
    else:
        print("{} |  -  |      -     | $ -".format(symbol))

        
df = df.astype({'after rebalancing': float})
print(x)
print(cash)