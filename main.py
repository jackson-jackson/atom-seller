import settings
import functions
from currencies import Bitcoin, Atom
import math
import time
import threading
from os import system

amount_sold = 0.0
num_orders = 0

# Work out rate for orders
def order_velocity():
    day = 24 * 60 * 60
    num_orders = settings.TARGET_VOLUME_DAY / settings.MIN_ORDER
    velocity = day / num_orders

    return velocity


# # Get average market order price of currency pair
# def get_average_price(currency_pair):    
#     orderbook = settings.POLO.returnOrderBook(settings.CURRENCY_PAIR, depth=5)
    
#     sum_price = 0

#     for ask in orderbook['bids']:
#        sum_price += float(ask[0])

#     return round(sum_price / len(orderbook['bids']), 8)


# Get price inside spread
def price_inside_spread(currency_pair):
        tickers = settings.POLO.returnTicker()
        highest_bid = float(tickers[settings.CURRENCY_PAIR]['highestBid'])
        lowest_ask = float(tickers[settings.CURRENCY_PAIR]['lowestAsk'])
        
        spread = lowest_ask - highest_bid

        order_price = highest_bid + (spread / 2)

        return round(order_price, 8)


# Sell ATOM
def sell():
    global num_orders, amount_sold

    price = price_inside_spread(settings.CURRENCY_PAIR)
    print(price)

    if Atom.price() > price and Atom.balance() > 0.5: # Above min price
        settings.POLO.sell(settings.CURRENCY_PAIR, price, settings.MIN_ORDER)
        num_orders += 1
        amount_sold += settings.MIN_ORDER


def cli_update():
    system('cls') # clear for linux, cls for Windows

    btc_price = Bitcoin.price()
    btc_balance = Bitcoin.balance()
    atom_balance = Atom.balance()
    atom_price = Atom.price()

    print("Atom Seller")
    print(" ")
    print(f"Current prices: BTC ${round(btc_price, 2)} USD; ATOM ${round(atom_price * btc_price, 2)} USD")
    print(" ")
    print(f"Target of {settings.TARGET_VOLUME_DAY} atoms per day, with minimum price of ${settings.MIN_PRICE} USD, and sell interval of {round(order_velocity())} seconds.")
    print(" ")
    print(f"Current BTC balance is {round(btc_balance, 2)} (${round(btc_balance * btc_price, 2)}), and ATOM balance is {round(atom_balance, 2)} (${round(atom_balance * atom_price * btc_price, 2)})")
    print(" ")
    print(f"Number of orders executed: {num_orders}")
    print(f"Total atoms sold: {amount_sold}")
    

def run_updates():
    cli_update()


def thread_one():
    threading.Timer(5, thread_one).start()
    run_updates()


def thread_two():
    time.sleep(5)
    threading.Timer(order_velocity(), thread_two).start()
    sell()


thread_one()
thread_two()