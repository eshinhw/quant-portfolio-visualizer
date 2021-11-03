import os
import time
import datetime as dt
from demo_credentials import OANDA_API_KEY, TEST_ACCOUNT_ID, VOLATILITY_BREAKOUT
from oandaTrader import OandaTrader
from trend_momentum import SYMBOLS_TRADES

# Login
if os.name == 'nt':
    oanda = OandaTrader(OANDA_API_KEY, VOLATILITY_BREAKOUT)
if os.name == 'posix':
    oanda = OandaTrader(OANDA_API_KEY, VOLATILITY_BREAKOUT)

ORDERS_LIST = oanda.get_order_list()
TRADES_LIST = oanda.get_trade_list()

SYMBOLS_ORDERS = oanda.symbols_in_orders()
SYMBOLS_TRADES = oanda.symbols_in_trades()

def manage_trades():
    for symbol in SYMBOLS_TRADES:
        for order in ORDERS_LIST:
            if order['type'] != 'STOP_LOSS' and symbol == order['instrument']:
                oanda.cancel_single_order(order['id'])

if __name__ == '__main__':
    manage_trades()
    print("Manage Trades::: " + time.ctime())