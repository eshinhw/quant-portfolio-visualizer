import json
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments

INSTRUMENTS = ["EUR_USD", "GBP_USD", 'AUD_USD', 'NZD_USD']
#INSTRUMENTS = ["EUR_USD"]
RISK_PER_TRADE = 0.001

POSITION_STATUS = {}


def update_position_status(pair, accountID):

    trades_list = get_trade_list(accountID)
    open_trades_inst = []
    for trade in trades_list:
        open_trades_inst.append(trade["instrument"])
    for pair in INSTRUMENTS:

        if (
            pair in POSITION_STATUS.keys()
            and POSITION_STATUS[pair] == 1
            and not (pair in open_trades_inst)
        ):
            POSITION_STATUS[pair] = 0


def cancel_all_trades(accountID):
    """ Cancel all open orders

    Args:
        accountID (String): account ID
    """
    order_list = get_order_list(accountID)
    # print("RESPONSE:\n{}".format(json.dumps(order_list, indent=2)))
    # print(order_list)
    for order in order_list:
        r = orders.OrderCancel(accountID=accountID, orderID=order["id"])
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
    return resp["orders"]


def get_trade_list(accountID):
    """ Retrieve a list of open trades

    Args:
        accountID (String): account ID

    Returns:
        List[String]: open trades
    """
    r = trades.TradesList(accountID)
    resp = client.request(r)
    #print("RESPONSE:\n{}".format(json.dumps(resp, indent=2)))
    return resp["trades"]


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
    (currentAsk, currentBid) = get_current_ask_bid_price("USD_CAD")
    acct_conversion_rate = 1 / ((currentAsk + currentBid) / 2)
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


def get_candle_data(symbol, count, interval):
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
        instrument=symbol, params=instrument_params)
    resp = client.request(r)
    return resp


def calculate_moving_average(symbol, count, interval):
    instrument_params = {"count": count + 1, "granularity": interval}

    r = instruments.InstrumentsCandles(
        instrument=symbol, params=instrument_params)
    resp = client.request(r)
    closes = []
    for day in resp["candles"]:
        if day["complete"] == True:
            closes.append(float(day["mid"]["c"]))

    return sum(closes) / len(closes)


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
    POSITION_STATUS[pair] = 1


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
    POSITION_STATUS[pair] = 1


def create_sell_limit(pair, entry, stop_loss, unit_size):
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GFD", "price": str(stop_loss)},
            "timeInForce": "GFD",
            "instrument": pair,
            "units": "-" + str(unit_size),
            "type": "LIMIT",
            "positionFill": "DEFAULT",
        }
    }
    r = orders.OrderCreate(accountID, data=order_body)
    client.request(r)
    POSITION_STATUS[pair] = 1
    print(
        f"LIMIT Trade Placed --- pair: {pair} | entry: {str(entry)} | stop_loss: {str(stop_loss)} | unit_size: {str(unit_size)}")


def create_buy_limit(pair, entry, stop_loss, unit_size):
    order_body = {
        "order": {
            "price": str(entry),
            "stopLossOnFill": {"timeInForce": "GFD", "price": str(stop_loss)},
            "timeInForce": "GFD",
            "instrument": pair,
            "units": str(unit_size),
            "type": "LIMIT",
            "positionFill": "DEFAULT",
        }
    }
    r = orders.OrderCreate(accountID, data=order_body)
    client.request(r)
    POSITION_STATUS[pair] = 1
    print(
        f"LIMIT Trade Placed --- pair: {pair} | entry: {str(entry)} | stop_loss: {str(stop_loss)} | unit_size: {str(unit_size)}")


# def create_buy_market(pair, stop_loss, unit_size):
#     order_body = {
#         "order": {
#             "price": str(entry),
#             "stopLossOnFill": {"timeInForce": "GFD", "price": str(stop_loss)},
#             "timeInForce": "GFD",
#             "instrument": pair,
#             "units": str(unit_size),
#             "type": "MARKET",
#             "positionFill": "DEFAULT",
#         }
#     }
#     r = orders.OrderCreate(accountID, data=order_body)
#     client.request(r)
#     POSITION_STATUS[pair] = 1


# def create_sell_market(pair, stop_loss, unit_size):
#     order_body = {
#         "order": {
#             "price": str(entry),
#             "stopLossOnFill": {"timeInForce": "GFD", "price": str(stop_loss)},
#             "timeInForce": "GFD",
#             "instrument": pair,
#             "units": str(unit_size),
#             "type": "MARKET",
#             "positionFill": "DEFAULT",
#         }
#     }
#     r = orders.OrderCreate(accountID, data=order_body)
#     client.request(r)
#     POSITION_STATUS[pair] = 1

def execute(accountID):
    # get two previous 4H candles & check ohlc -> c0, c1
    for pair in INSTRUMENTS:
        update_position_status(pair, accountID)

        q = 0.95
        rk = 1.5
        entry_buffer = 0.0003

        candles = get_candle_data(pair, 3, "H4")["candles"]
        base = candles[0]
        signal = candles[1]
        current = candles[2]

        signal_close = float(signal["mid"]["c"])
        signal_range = float(signal["mid"]["h"]) - float(signal["mid"]["l"])
        signal_upper_close_threshold = float(
            signal["mid"]["l"]) + (signal_range * q)
        signal_lower_close_threshold = float(
            signal["mid"]["h"]) - (signal_range * q)

        base_high = float(base["mid"]["h"])
        base_low = float(base["mid"]["l"])
        base_range = float(base["mid"]["h"]) - float(base["mid"]["l"])
        # print(signal_upper_close_threshold)
        # print(signal_range)
        # print(base_range)

        # buy setup
        if (
            signal_close > base_high
            and signal_close > signal_upper_close_threshold
            and signal_range > (base_range * rk)
        ):
            if POSITION_STATUS[pair] == 0:
                entry = float(current["mid"]["o"]) - entry_buffer
                stop_loss = float(signal["mid"]["l"])
                unit_size = calculate_unit_size(entry, stop_loss)
                create_buy_limit(pair, entry, stop_loss, unit_size)
            else:
                continue

        # sell setup
        if (
            signal_close < base_low
            and signal_close < signal_lower_close_threshold
            and signal_range > (base_range * rk)
        ):
            if POSITION_STATUS[pair] == 0:
                entry = float(current["mid"]["o"]) + entry_buffer
                stop_loss = float(signal["mid"]["l"])
                unit_size = calculate_unit_size(entry, stop_loss)
                create_sell_limit(pair, entry, stop_loss, unit_size)
            else:
                continue
    # if that's true: buy at current open + stop loss at previous candle's high or low

    # when the current candle is complete, move stop to current candle's high or low

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


if __name__ == '__main__':

    with open("oanda_demo_api_token.txt", "r") as secret:
        contents = secret.readlines()
        api_token = contents[0].rstrip("\n")
        accountID = contents[1]
        secret.close()

    client = API(access_token=api_token)

    execute(accountID)
