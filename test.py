import json
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments


INSTRUMENTS = ['EUR_USD']


def get_acct_summary(accountID):
    r = accounts.AccountSummary(accountID)
    resp = client.request(r)
    print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))
    return resp


def get_price_data(symbol):
    instrument_params = {'count': 2, 'granularity': 'D'}

    r = instruments.InstrumentsCandles(instrument="EUR_USD",
                                       params=instrument_params)
    resp = client.request(r)
    print("RESPONSE:\n{}".format(json.dumps(resp, indent=2)))
    return resp


def get_trade_list():
    r = trades.TradesList(accountID)
    # show the endpoint as it is constructed for this call
    print("REQUEST:{}".format(r))
    rv = client.request(r)
    print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))

def get_current_price(pair):

    params = {
          "instruments": pair
        }
    r = pricing.PricingInfo(accountID=accountID, params=params)
    rv = client.request(r)
    print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))
    return rv


def create_buy_stop(pair, entry, stopLoss):
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {
                "timeInForce": "GFD",
                "price": str(stopLoss)
            },
            "timeInForce": "GFD",
            "instrument": "EUR_USD",
            "units": "100",
            "type": "STOP",
            "positionFill": "DEFAULT"
        }
    }

    r = orders.OrderCreate(accountID, data=order_body)
    client.request(r)
    #print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))


def create_sell_stop(pair, entry, stopLoss):
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {
                "timeInForce": "GFD",
                "price": str(stopLoss)
            },
            "timeInForce": "GFD",
            "instrument": "EUR_USD",
            "units": "-100",
            "type": "STOP",
            "positionFill": "DEFAULT"
        }
    }

    r = orders.OrderCreate(accountID, data=order_body)
    client.request(r)
    #print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))

# Initialize OANDA API Client

with open('oanda_demo_api_token.txt', 'r') as secret:
    contents = secret.readlines()
    print(contents)
    api_token = contents[0].rstrip('\n')
    accountID = contents[1]
    secret.close()

client = API(access_token=api_token)

# Get previous day's range

#while True:

for pair in INSTRUMENTS:
    data = get_price_data(pair)
    #print(data)
    prev_high = float(data['candles'][0]['mid']['h'])
    prev_low = float(data['candles'][0]['mid']['l'])
    prev_range = prev_high - prev_low
    k = 0.6
    rangeK = prev_range * k


    today_open = float(data['candles'][1]['mid']['o'])
    #print(today_open)
    currentPrice = get_current_price(pair)
    currentAsk = currentPrice['prices'][0]['closeoutAsk']
    currentBid = currentPrice['prices'][0]['closeoutBid']

    print(currentAsk, currentBid)
    #print(currentPrice)
    # buy stop order at today_open + rangeK

    buy_stop = today_open + rangeK
    sell_stop = today_open - rangeK

    #create_buy_stop(pair, buy_stop, today_open)
    create_sell_stop(pair, sell_stop, today_open)
    stop_loss = buy_stop - today_open
    take_profit = 2 * stop_loss

    print(f'buy stop: {buy_stop}, sell stop: {sell_stop}')
    print(f'stop loss: {stop_loss}, take profit: {take_profit}')





