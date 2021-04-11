import time
import oanda
import schedule
import turtle_soup
#import original_turtle

if __name__ == "__main__":

    # original turtle trend following system
    # original_turtle.check_trade_conditions()
    # original_turtle.update_position_status()

    # turtle soup reversal system at prev highs and lows
    turtle_soup.check_trade_conditions()
    turtle_soup.update_order_trade_status()

    # volatility breakout based on prev day's range
    # vol_breakout.check_trade_conditions()
    # vol_breakout.update_order_trade_status()

    # cancel all pending order before weekend
    schedule.every().sunday.at("17:00").do(oanda.cancel_all_orders)
    schedule.every().friday.at("16:30").do(oanda.cancel_all_orders)

    while True:
        schedule.run_pending()
        time.sleep(3)
