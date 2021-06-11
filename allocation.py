import questrade
import pprint


qbot = questrade.qbot()

# usd_bal = qbot.get_usd_total_equity()

# positions = qbot.get_acct_positions()

# print(usd_bal)

# print(positions)

#print(qbot.get_ticker_info('TLT'))

# total equity (market value + cash)

# current market value (invested asset)

# cash portion

# stock vs cash weight

stock_weight = 0.7
numStocks = 15

usd_equity = qbot.get_usd_total_equity()



amount_per_stock = (usd_equity * stock_weight) / numStocks
print(amount_per_stock)
print(amount_per_stock * numStocks)

print(qbot.get_positions())



"""
equity * stock weight = total market value in stock

total market value in stock / 15 stocks = market value for each stock

unused portion of stock = total market value in stock - current market value

BUY RULES

15% from recent high = 0.3%
25% from recent high = 0.3%
50% from recent high = 0.4%

WHEN TO SELL


"""