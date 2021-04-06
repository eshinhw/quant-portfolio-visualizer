import json
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments


INSTRUMENTS = ['EUR_USD', 'GBP_USD', 'USD_JPY', 'USD_CAD']


def get_acct_summary(accountID):
    r = accounts.AccountSummary(accountID)
    resp = client.request(r)
    print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))
    return resp


def get_price_data(symbol):
    instrument_params = {'count': 2, 'granularity': 'D'}

    r = instruments.InstrumentsCandles(instrument=symbol,
                                       params=instrument_params)
    resp = client.request(r)
    #print("RESPONSE:\n{}".format(json.dumps(resp, indent=2)))
    return resp


def calculate_moving_average(symbol):
    instrument_params = {'count': 21, 'granularity': 'D'}

    r = instruments.InstrumentsCandles(instrument=symbol,
                                       params=instrument_params)
    resp = client.request(r)
    print(len(resp['candles']))
    closes = []
    for day in resp['candles']:
        if day['complete'] == True:
            closes.append(float(day['mid']['c']))

    return sum(closes)/len(closes)
    #print("RESPONSE:\n{}".format(json.dumps(resp, indent=2)))

def get_trade_list():
    r = trades.TradesList(accountID)
    # show the endpoint as it is constructed for this call
    #print("REQUEST:{}".format(r))
    rv = client.request(r)
    #print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))

def get_current_price(pair):

    params = {
          "instruments": pair
        }
    r = pricing.PricingInfo(accountID=accountID, params=params)
    rv = client.request(r)
    #print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))
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
            "instrument": pair,
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
            "instrument": pair,
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
    #print(contents)
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

    #print(currentAsk, currentBid)
    #print(currentPrice)
    # buy stop order at today_open + rangeK
    buy_stop = today_open + rangeK
    sell_stop = today_open - rangeK
    twenty_ma = calculate_moving_average(pair)

    print(f'Symbol: {pair}, Today_Open: {today_open}, prev_high: {prev_high}, prev_low: {prev_low}, buy_stop: {buy_stop}, sell_stop: {sell_stop}, twenty_ma: {twenty_ma}')

    # print(twenty_ma)

    if today_open < twenty_ma: # bearish
        if 'JPY' in pair:
            create_sell_stop(pair, round(sell_stop,3), round(today_open,3))
        else:
            create_sell_stop(pair, round(sell_stop,5), round(today_open,5))
    if today_open > twenty_ma: # bullish
        if 'JPY' in pair:
            create_buy_stop(pair, round(buy_stop,3), round(today_open,3))
        else:
            create_buy_stop(pair, round(buy_stop,3), round(today_open,5))



    #print(f'buy stop: {buy_stop}, sell stop: {sell_stop}')
    #print(f'stop loss: {stop_loss}, take profit: {take_profit}')





