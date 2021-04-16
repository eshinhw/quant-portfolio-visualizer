import json
import time
import oanda
import schedule
import turtle_soup
#import original_turtle

if __name__ == "__main__":

    with open('./account_info.json', 'r') as fp:
        accounts = json.load(fp)

    # # cancel all pending order before weekend
    schedule.every().sunday.at("17:00").do(oanda.cancel_all_orders)
    schedule.every().friday.at("16:30").do(oanda.cancel_all_orders)

    while True:
        schedule.run_pending()
        turtle_soup.check_condition_and_place_orders(accounts['turtle_soup'])
        oanda.update_order_trade_status(accounts['turtle_soup'])
        time.sleep(3)
    # print(oanda.get_order_list(accounts['turtle_soup']))

    # long_id = oanda.find_order_id(accounts['turtle_soup'], 'EUR_USD', 'LONG')
    # short_id = oanda.find_order_id(accounts['turtle_soup'], 'EUR_USD', 'SHORT')

    # print(short_id)

    # print(oanda.get_order_details(accounts['turtle_soup'], long_id))
    # print(oanda.get_order_details(accounts['turtle_soup'], short_id))
