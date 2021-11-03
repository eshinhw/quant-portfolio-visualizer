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

INSTRUMENTS = oanda.fx_instruments()

RISK_PER_TRADE = 0.001

ORDERS_LIST = oanda.get_order_list()
TRADES_LIST = oanda.get_trade_list()

SYMBOLS_ORDERS = oanda.symbols_in_stop_orders()
SYMBOLS_TRADES = oanda.symbols_in_trades()

DECIMAL_TABLE = oanda.create_decimal_table()

def manage_trades():
    for trade in TRADES_LIST:
        instrument = trade['instrument']
        if instrument in SYMBOLS_ORDERS:
            for order in ORDERS_LIST:
                order_id = order['id']
                if instrument == order['instrument']:
                    oanda.cancel_single_order(order_id)

if __name__ == '__main__':
    manage_trades()
    print("Manage Trades::: " + time.ctime())