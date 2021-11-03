import os
import time
import datetime as dt
from demo_credentials import OANDA_API_KEY, TEST_ACCOUNT_ID, VOLATILITY_BREAKOUT
from oandaTrader import OandaTrader

# Login
if os.name == 'nt':
    oanda = OandaTrader(OANDA_API_KEY, VOLATILITY_BREAKOUT)
if os.name == 'posix':
    oanda = OandaTrader(OANDA_API_KEY, VOLATILITY_BREAKOUT)

ORDERS_LIST = oanda.get_order_list()
TRADES_LIST = oanda.get_trade_list()

def manage_trades():
    for trade in TRADES_LIST:
        #print(trade)
        trade_id = trade['id']
        trade_instrument = trade['instrument']
        for order in ORDERS_LIST:
            if order['type'] == 'LIMIT' and trade_instrument == order['instrument']:
                print(order)
                oanda.cancel_single_order(order['id'])

if __name__ == '__main__':
    manage_trades()
    manage_trades()
    manage_trades()
    manage_trades()
    manage_trades()
    print("Manage Trades::: " + time.ctime())