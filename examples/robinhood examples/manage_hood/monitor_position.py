
#!/usr/bin/env python
# import necessary modules
import itertools
import time
from robin_stocks import robinhood as r
from rh_two_factor_log_in import loginmfa

def is_price_near_strike(price, strike, tolerance):
    return (abs(price - strike) < tolerance)

loginmfa()


def waiting_spinner(interval):
    """Show a waiting spinner"""
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    for _ in range(10 * interval):
        print(next(spinner), end='\r')
        time.sleep(0.1)

interval = 30 # in seconds

# set up infinite loop that runs every 5 minutes
while True:
    # get option positions
    option_positions = r.options.get_open_option_positions()

    # loop through each position and print out the details
    for pos in option_positions:
        print("Position:")
        print("Symbol:", pos['chain_symbol'])
        print("Position type:", pos['type'])
        print("Quantity:", pos['quantity'])
        print("Average price:", pos['average_price'])
        print("Date opened:", pos['created_at'])

        oid = r.options.get_option_instrument_data_by_id(pos['option_id'])
        print("Option type:", oid['type'])

        omd = r.options.get_option_market_data_by_id(pos['option_id'])[0]
        print("high fill rate buy price:", omd['high_fill_rate_buy_price'])
        print("high fill rate sell price:", omd['high_fill_rate_sell_price'])
        print("-----------------------------")
        print()

        # get underlying symbol
        underlying = pos['chain_symbol']

        # get current price of underlying symbol
        current_price = float(r.stocks.get_latest_price(underlying)[0])
        print("Current price of underlying:", current_price)

        option_strike_price = float(oid['strike_price'])
        print("Option Strike price:", option_strike_price)

        # check if current price of underlying is equal to strike price of instrument
        if is_price_near_strike(current_price, option_strike_price, tolerance=.3):
            print("Current price of underlying is near Strike price of instrument.")
        else:
            print(
                "Current price of underlying is not near Strike price of instrument.")
        print("-----------------------------")
        print()

    print("Waiting for {} seconds".format(interval))
    waiting_spinner(interval)
    print("-----------------------------")
