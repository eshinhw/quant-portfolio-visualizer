import os
import time
from oanda import Oanda
from credentials import API_OANDA, VB_ACCT, DEMO_ACCT


# Login
if os.name == 'nt':
    oanda = Oanda(API_OANDA, VB_ACCT)
if os.name == 'posix':
    oanda = Oanda(API_OANDA, DEMO_ACCT)


# Login
if os.name == 'nt':
    oanda = Oanda(API_OANDA, DEMO_ACCT)
if os.name == 'posix':
    oanda = Oanda(API_OANDA, DEMO_ACCT)

def close_trades():
    oanda.cancel_all_orders()
    oanda.close_all_trades()

if __name__ == '__main__':
    close_trades()
