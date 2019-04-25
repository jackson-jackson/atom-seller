import poloniex
import private
from currencies import Bitcoin, Atom
import math
import time
import threading
from os import system


polo = poloniex.Poloniex(private.API_KEY,private.API_SECRET)

# Configuration
target_volume_day = 10 # Target amount of atoms that the script should sell per day
min_atom_price = 3 # Minimum atom price in USD that the script should sell at. Script will not sell below this

min_order = .25 #TODO make this based on min btc order size of .0001

currency_pair = 'BTC_ATOM'

amount_sold = 0.0
num_orders = 0


# Work out rate for orders
def order_velocity():
    day = 24 * 60 * 60
    num_orders = target_volume_day / min_order
    velocity = day / num_orders

    return velocity


def update_balances():
    Bitcoin.balance()
    Atom.balance()


# Get average price of currency pair
def get_average_price(currency_pair):    
    orderbook = polo.returnOrderBook(currency_pair, depth=5)
    
    sum_price = 0

    for ask in orderbook['bids']:
       sum_price += float(ask[0])

    return round(sum_price / len(orderbook['bids']), 8)


def sell():
    global num_orders, amount_sold

    price = get_average_price(currency_pair)

    if Atom.price() > price and Atom.balance() > 0.5: # Above min price
        polo.sell(currency_pair, price, min_order)
        num_orders += 1
        amount_sold += min_order


def cli_update():
    system('cls') # clear for linux, cls for Windows

    print("Atom Seller")
    print(" ")
    print(f"Current prices: BTC ${round(Bitcoin.price(), 2)} USD; ATOM ${round(Atom.price() * Bitcoin.price(), 2)} USD")
    print(" ")
    print(f"Target of {target_volume_day} atoms per day, with minimum price of ${min_atom_price} USD, and sell interval of {round(order_velocity())} seconds.")
    print(" ")
    print(f"Current BTC balance is {round(Bitcoin.balance(), 2)} (${round(Bitcoin.balance() * Bitcoin.price(), 2)}), and ATOM balance is {round(Atom.balance(), 2)} (${round(Atom.balance() * Atom.price() * Bitcoin.price(), 2)})")
    print(" ")
    print(f"Number of orders executed: {num_orders}")
    print(f"Total atoms sold: {amount_sold}")
    

def run_updates():
    update_balances()
    cli_update()


def thread_one():
    threading.Timer(10, thread_one).start()
    run_updates()


def thread_two():
    time.sleep(10)
    threading.Timer(order_velocity(), thread_two).start()
    sell()


thread_one()
thread_two()