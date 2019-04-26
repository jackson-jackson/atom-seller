import settings
import functions
from currencies import Bitcoin, Atom
import math
import time
import threading
from os import system

amount_sold = 0.0
num_orders = 0
open_orders_total = 0.0


# Work out rate for orders
def order_velocity():
    day = 24 * 60 * 60

    price = price_inside_spread(settings.CURRENCY_PAIR)

    # Determine min order
    min_order = settings.MIN_ORDER / price

    num_orders = settings.TARGET_VOLUME_DAY / min_order
    velocity = day / num_orders

    return velocity


# Get price inside spread
def price_inside_spread(currency_pair):
        tickers = settings.POLO.returnTicker()
        highest_bid = float(tickers[settings.CURRENCY_PAIR]['highestBid'])
        lowest_ask = float(tickers[settings.CURRENCY_PAIR]['lowestAsk'])
        
        spread = lowest_ask - highest_bid

        order_price = highest_bid + (spread / 2)

        return round(order_price, 8)


# Get total number of ATOM in open orders
def get_open_orders_total():
    orders = settings.POLO.returnOpenOrders('BTC_ATOM')
    open_orders = []

    for order in orders:
        open_orders.append(float(order['total']))
    return round(sum(open_orders), 8)


# Place limit order
def place_order():
    global num_orders, amount_sold

    price = price_inside_spread(settings.CURRENCY_PAIR)

    # Determine min order
    min_order = settings.MIN_ORDER / price

    if Atom.price() > price and Atom.balance() > 0.5:
        settings.POLO.sell(settings.CURRENCY_PAIR, price, min_order)
        num_orders += 1
        amount_sold += min_order


def cli_update():
    

    btc_price = Bitcoin.price()
    btc_balance = Bitcoin.balance()
    atom_balance = Atom.balance()
    atom_price = Atom.price()

    open_orders = functions.open_orders()
    open_orders_total = get_open_orders_total()
    order_vel = order_velocity()

    if settings.OS == 'LINUX':
        system('clear') # clear for linux, cls for Windows
    else:
        system('cls')

    print("Atom Seller")
    print(" ")
    print(f"Current prices: :::: BTC ${round(btc_price, 2)} USD :::: ATOM ${round(atom_price * btc_price, 2)} USD ::::")
    print(" ")
    print(f"Target of {settings.TARGET_VOLUME_DAY} ATOM per day, with minimum price of ${settings.MIN_PRICE} USD, and sell interval of {round(order_vel)} seconds.")
    print(" ")
    print(f"Current BTC balance is {round(btc_balance, 2)} (${round(btc_balance * btc_price, 2)}), and ATOM balance is {round(atom_balance, 2)} (${round(atom_balance * atom_price * btc_price, 2)})")
    print(" ")
    print(f"Number of orders executed: {num_orders}")
    print(f"Total ATOM sold: {amount_sold}")
    print(f"Number of open orders: {len(open_orders)}")
    print(f"Total ATOM in open orders: {open_orders_total}")
    

def run_updates():
    cli_update()


def thread_one():
    threading.Timer(10, thread_one).start()
    run_updates()


def thread_two():
    time.sleep(5)
    threading.Timer(order_velocity(), thread_two).start()
    place_order()


thread_one()
thread_two()