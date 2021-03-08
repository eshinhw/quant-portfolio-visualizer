# get a list of trades
# from oandapyV20 import API
import oandapyV20
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.instruments as instruments
import json
import pandas as pd

# api = API(access_token="0ca9619de6d428b6fdbcb4d20ef81268-cca1610e83cde7da5395d4468c2c1fe9")
# accountID = "101-002-5334779-003"

# r = trades.TradesList(accountID)
# # show the endpoint as it is constructed for this call
# print("REQUEST:{}".format(r))
# rv = api.request(r)
# print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))


client = oandapyV20.API(access_token="0ca9619de6d428b6fdbcb4d20ef81268-cca1610e83cde7da5395d4468c2c1fe9")
params = {"count": 12, "granularity": "M"}
r = instruments.InstrumentsCandles(instrument="EUR_USD",
                                   params=params)
rv = client.request(r)
#print(json.dumps(rv, indent=2))
monthly_candles = rv['candles']

columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
monthlyPrices = pd.DataFrame(columns)

for m in monthly_candles:
    print(m['mid']['c'])
    print()
