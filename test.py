import json
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments

INSTRUMENTS = ["EUR_USD", "GBP_USD", "USD_JPY", "USD_CAD"]
RISK_PER_TRADE = 0.001


def cancel_all_trades(accountID):
    """ Cancel all open orders

    Args:
        accountID (String): account ID
    """
    order_list = get_order_list(accountID)
    #print("RESPONSE:\n{}".format(json.dumps(order_list, indent=2)))
    # print(order_list)
    for order in order_list:
        r = orders.OrderCancel(accountID=accountID, orderID=order['id'])
        client.request(r)


def get_order_list(accountID):
    """ Retrieve a list of open orders

    Args:
        accountID (String): account ID

    Returns:
        List[String]: open orders
    """
    r = orders.OrderList(accountID)
    resp = client.request(r)
    return resp['orders']


def get_account_conversion_rate():
    """ Base currency of the account is CAD so pip value should be converted to CAD from other base currencies.

    Returns:
        Float: CAD/USD exchange rate
    """
    (currentAsk, currentBid) = get_current_ask_bid_price("USD_CAD")
    return 1 / ((currentAsk + currentBid) / 2)


def calculate_unit_size(entry, stop_loss):
    """ Calculate unit size per trade (fixed % risk per trade assigned in RISK_PER_TRADE).

    Args:
        entry (Float): entry price
        stop_loss (Float): stop loss price

    Returns:
        Float: unit size
    """
    account_balance = get_acct_summary(accountID)
    risk_amt_per_trade = account_balance * RISK_PER_TRADE
    entry = round(entry, 4)
    stop_loss = round(stop_loss, 4)
    stop_loss_pips = round(abs(entry - stop_loss) * 10000, 0)
    acct_conversion_rate = get_account_conversion_rate()
    unit_size = round(
        (risk_amt_per_trade / stop_loss_pips * acct_conversion_rate) * 10000, 0
    )
    return unit_size


def get_acct_summary(accountID):
    """ Retrieve account balance.

    Args:
        accountID (String): account ID

    Returns:
        Float: current account balance
    """
    resp = client.request(accounts.AccountSummary(accountID))
    return float(resp["account"]["balance"])


def get_price_data(symbol, count, interval):
    """ Return historical price data.

    Args:
        symbol (String): symbol
        count (Int): number of intervals
        interval (String): Daily 'D', Weekly 'W', ...

    Returns:
        JSON: json format in python dictionary
    """
    instrument_params = {"count": count, "granularity": interval}

    r = instruments.InstrumentsCandles(
        instrument=symbol, params=instrument_params
    )
    resp = client.request(r)
    return resp


def calculate_moving_average(symbol, count, interval):
    instrument_params = {"count": count + 1, "granularity": interval}

    r = instruments.InstrumentsCandles(
        instrument=symbol, params=instrument_params
    )
    resp = client.request(r)
    closes = []
    for day in resp["candles"]:
        if day["complete"] == True:
            closes.append(float(day["mid"]["c"]))

    return sum(closes) / len(closes)


def get_trade_list():
    r = trades.TradesList(accountID)
    # show the endpoint as it is constructed for this call
    # print("REQUEST:{}".format(r))
    rv = client.request(r)
    print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))


def get_current_ask_bid_price(pair):
    """ Return current ask and bid price for pair

    Args:
        pair (String): currency pair

    Returns:
        Tuple: (ask price, bid price)
    """

    r = pricing.PricingInfo(accountID=accountID, params={"instruments": pair})
    resp = client.request(r)
    ask_price = float(resp["prices"][0]["closeoutAsk"])
    bid_price = float(resp["prices"][0]["closeoutBid"])
    return (ask_price, bid_price)


def create_buy_stop(pair, entry, stop_loss, unit_size):
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GFD", "price": str(stop_loss)},
            "timeInForce": "GFD",
            "instrument": pair,
            "units": str(unit_size),
            "type": "STOP",
            "positionFill": "DEFAULT",
        }
    }
    r = orders.OrderCreate(accountID, data=order_body)
    client.request(r)


def create_sell_stop(pair, entry, stop_loss, unit_size):
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GFD", "price": str(stop_loss)},
            "timeInForce": "GFD",
            "instrument": pair,
            "units": "-" + str(unit_size),
            "type": "STOP",
            "positionFill": "DEFAULT",
        }
    }
    r = orders.OrderCreate(accountID, data=order_body)
    client.request(r)


# Initialize OANDA API Client
with open("oanda_demo_api_token.txt", "r") as secret:
    contents = secret.readlines()
    api_token = contents[0].rstrip("\n")
    accountID = contents[1]
    secret.close()

client = API(access_token=api_token)

cancel_all_trades(accountID)

# while True:

# for pair in INSTRUMENTS:
#     data = get_price_data(pair)
#     # print(data)
#     prev_high = float(data['candles'][0]['mid']['h'])
#     prev_low = float(data['candles'][0]['mid']['l'])
#     prev_range = prev_high - prev_low
#     k = 0.6
#     rangeK = prev_range * k

#     today_open = float(data['candles'][1]['mid']['o'])
#     # print(today_open)
#     #print(currentAsk, currentBid)
#     # print(currentPrice)
#     # buy stop order at today_open + rangeK
#     buy_stop = today_open + rangeK
#     sell_stop = today_open - rangeK
#     twenty_ma = calculate_moving_average(pair)

#     print(f'Symbol: {pair}, Today_Open: {today_open}, prev_high: {prev_high}, prev_low: {prev_low}, buy_stop: {buy_stop}, sell_stop: {sell_stop}, twenty_ma: {twenty_ma}')
#     if '_USD' in pair:

# if today_open < twenty_ma: # bearish
#     if 'JPY' in pair:
#         create_sell_stop(pair, round(sell_stop,3), round(today_open,3))
#     else:
#         # sell_stop = round(sell_stop,5)
#         # today_open = round(today_open,5)
#         # stopLoss_pips = abs()
#         create_sell_stop(pair, round(sell_stop,5), round(today_open,5))
# if today_open > twenty_ma: # bullish
#     if 'JPY' in pair:
#         create_buy_stop(pair, round(buy_stop,3), round(today_open,3))
#     else:
#         create_buy_stop(pair, round(buy_stop,3), round(today_open,5))

# print(f'buy stop: {buy_stop}, sell stop: {sell_stop}')
# print(f'stop loss: {stop_loss}, take profit: {take_profit}')
