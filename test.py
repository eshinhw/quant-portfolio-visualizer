import json
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments

INSTRUMENTS = ['EUR_USD']

def get_acct_summary(accountID):
    r = accounts.AccountSummary(accountID)
    resp = api.request(r)
    print ("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))
    return resp.json()

def get_price_data(symbol):
    instrument_params = {'count': 2, 'granularity': 'D'}

    r = instruments.InstrumentsCandles(instrument="EUR_USD",
                                        params=instrument_params)
    resp = api.request(r)
    print ("RESPONSE:\n{}".format(json.dumps(resp, indent=2)))
    return resp.json()

def get_trade_list():
    r = trades.TradesList(accountID)
    #show the endpoint as it is constructed for this call
    print("REQUEST:{}".format(r))
    rv = api.request(r)
    print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))

def create_buy_stop():

# Initialize OANDA API Client

with open('oanda_demo_api_token.txt', 'r') as secret:
    contents = secret.readlines()
    print(contents)
    api_token = contents[0].rstrip('\n')
    accountID = contents[1]
    secret.close()

client = API(access_token=api_token)









prev_high = float(resp['candles'][0]['mid']['h'])
prev_low = float(resp['candles'][0]['mid']['l'])

prev_range = prev_high - prev_low
print(prev_high, prev_low)
print(prev_range)
k = 0.6
rangeK = prev_range * k
print(rangeK)

today_open = float(resp['candles'][1]['mid']['o'])
print(today_open)

# buy stop order at today_open + rangeK

buy_stop = today_open + rangeK
sell_stop = today_open - rangeK

print(today_open)
print(buy_stop, sell_stop)

stop_loss = buy_stop - today_open
take_profit = 2 * stop_loss

print(stop_loss, take_profit)
# sell stop order at today_open - rangeK

order_body = {
  "order": {
    "price": "1.20",
    "stopLossOnFill": {
      "timeInForce": "GTC",
      "price": "1.17"
    },
    "timeInForce": "GTC",
    "instrument": "EUR_USD",
    "units": "100",
    "type": "STOP",
    "positionFill": "DEFAULT"
  }
}


r = orders.OrderCreate(accountID, data=order_body)
rv = api.request(r)

print ("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))



