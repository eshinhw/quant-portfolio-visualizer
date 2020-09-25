import questrade as qt
import pandas as pd
from prettytable import PrettyTable
import sys
import portfolios

DIVIDER = "=" * 60

# input target allocation ratio bewteen two assets
#target = {'VFV.TO': 0.7, 'XBB.TO': 0.3}

weights = portfolios.get_user_input()

try:
    if sum(weights.values()) < 0 or sum(weights.values()) > 1:
        raise Exception
        
except:
    print("Invalid Portfolio Inputs")
    sys.exit()

# check if assets in selected portfolio are tradeable in Questrade 

try:
    for symbol in weights.keys():
        
        if qt.check_symbol_exists(symbol) == False:
            nta = symbol
            raise Exception
except:
    print('PORTFOLIO CONTAINS A NON-TRADABLE ASSET {}'.format(nta))
    sys.exit()  
    
else:
    print()
    print(DIVIDER)
    print("TARGET ALLOCATION")
    print(DIVIDER)
    for symbol in weights:
            print("{} : {} %".format(symbol,weights[symbol] * 100))        

# input transaction cost for selling assets
transaction = 5

acctNum = qt.get_account_num()[0]

totalEquity = qt.get_active_balance_cad(acctNum)['totalEquity']
prior_cash = qt.get_active_balance_cad(acctNum)['cash']
post_cash = prior_cash

# returns a list of positions called position
# where each element is a dictionary containing position info for each position
positions = qt.get_open_positions(acctNum)

# output dataframe for rebalancing calculation
df = pd.DataFrame()

# print(positions)
currentHoldings = []

# add currently holding positions into dataframe from a list of positions
for position in positions:    
    
    symbol = position['symbol']
    openQuantity = position['openQuantity']
    currMV = position['currentMarketValue']
    currPrice = position['currentPrice']  
    #print(position)
    currentHoldings.append(symbol)
    
    df = df.append(position, ignore_index=True)   
    
# print(df)
# print(currentHoldings)

# add newly added assets into dataframe

for symbol in weights.keys():
    
    # print("weights symbol: ", symbol)
    # print(df['symbol'])
    
    if symbol not in currentHoldings:
        
        # print("not in current portfolio: " ,symbol)
        new = {}
        new['symbol'] = symbol
        new['openQuantity'] = 0
        new['currentMarketValue'] = 0
        new['currentPrice'] = qt.get_current_price(symbol)
        new['symbolId'] = qt.get_symbol_id(symbol)
        
        df = df.append(new, ignore_index=True)

df.set_index('symbol', inplace=True)

# calculate quantity changes for rebalancing

for symbol in df.index:
    if symbol not in weights: # we have to sell all shares of symbol
        df.loc[symbol, 'targetValue'] = 0
        df.loc[symbol,'variation'] = df.loc[symbol,'targetValue'] - df.loc[symbol,'currentMarketValue']  
        df.loc[symbol,'Qty Change'] = df.loc[symbol,'variation'] / df.loc[symbol,'currentPrice']
    else:
                    
        df.loc[symbol,'targetValue'] = (totalEquity * weights[symbol])
        df.loc[symbol,'variation'] = df.loc[symbol,'targetValue'] - df.loc[symbol,'currentMarketValue']  
        df.loc[symbol,'Qty Change'] = df.loc[symbol,'variation'] / df.loc[symbol,'currentPrice']
    
# change datatype for certain columns

df = df.astype({'Qty Change': int, 'symbolId': int, 'openQuantity': int})

# sort by qty change so that we can sell some first and buy other later with more cash

df.sort_values(by=['Qty Change'], inplace=True)

# iterate from the top to sell first and buy later with cash adjustment

rebal = PrettyTable()

rebal.field_names = ['SYMBOL', 'ACTION REQ.', '# SHARES', 'PRICE']

for symbol in df.index:

    qty = df.loc[symbol,'Qty Change']
    currP = df.loc[symbol, 'currentPrice']
    
    # buying
    if qty > 0:
        buy = qty * currP
        
        if post_cash < buy:
            new_qty = int(post_cash / currP)
            buy = currP * new_qty
            qty = new_qty            
        post_cash = post_cash - buy
        df.loc[symbol, 'after rebalancing'] = df.loc[symbol, 'currentMarketValue'] + buy
        rebal.add_row([symbol, 'BUY', int(qty), "$ {:.2f}".format(currP)])
        #print("Total ${} is subtracted from cash account".format(buy))
    
    # selling
    elif qty < 0:
        sell = (-qty) * currP
        post_cash = post_cash + sell - transaction
        df.loc[symbol, 'after rebalancing'] = df.loc[symbol, 'currentMarketValue'] - sell
        rebal.add_row([symbol, 'SELL', -int(qty), "$ {:.2f}".format(currP)])
        #print("Total ${} is added from cash account".format(sell))
    
    # no rebalancing
    else:
        df.loc[symbol, 'after rebalancing'] = df.loc[symbol, 'currentMarketValue']
        rebal.add_row([symbol, '-', '-', "$ -"])

        
df = df.astype({'after rebalancing': float})

summary = PrettyTable()

summary.field_names = ['ASSETS', 'PRIOR ($)', 'PRIOR (%)', 'POST ($)', 'POST (%)']

summary.add_row(['CASH', 
                 "$ {:.2f}".format(prior_cash), 
                 "{:.2f} %".format((prior_cash/totalEquity)*100),
                 "$ {:.2f}".format(post_cash),                   
                 "{:.2f} %".format((post_cash/totalEquity)*100)])

for symbol in df.index:
    priorMV = df.loc[symbol,'currentMarketValue']
    postMV = df.loc[symbol, 'after rebalancing']
    
    summary.add_row([symbol, 
                     "$ {:.2f}".format(priorMV),
                     "{:.2f} %".format((priorMV/totalEquity)*100),
                     "$ {:.2f}".format(postMV),                      
                     "{:.2f} %".format((postMV/totalEquity)*100)])
    
print()
rebal.sortby = 'ACTION REQ.'
rebal.reversesort = True
print(rebal.get_string(title="REBALANCING ORDER SUMMARY"))
print()
summary.sortby = 'POST (%)'
summary.reversesort = True
print(summary.get_string(title="POST-REBALANCING ACCOUNT STATUS OVERVIEW"))

