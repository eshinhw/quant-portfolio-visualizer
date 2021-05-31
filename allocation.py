import questrade
import pprint


qbot = questrade.qbot()

# usd_bal = qbot.get_usd_total_equity()

# positions = qbot.get_acct_positions()

# print(usd_bal)

# print(positions)

print(qbot.get_ticker_info('TLT'))