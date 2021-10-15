import json
from demo_credentials import OANDA_API_KEY, VOL_BREAKOUT_ACCOUNT_ID
# get a list of trades
from oandapyV20 import API
import oandapyV20.endpoints.trades as trades

api = API(access_token=OANDA_API_KEY)
accountID = VOL_BREAKOUT_ACCOUNT_ID

r = trades.TradesList(accountID)
# show the endpoint as it is constructed for this call
print("REQUEST:{}".format(r))
rv = api.request(r)
print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))