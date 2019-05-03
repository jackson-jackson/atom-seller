import settings
import poloniex
import private
from exchanges import Poloniex, Kraken
import math
import time
import threading
from os import system
import logging
import json


# Setup logging
logging.basicConfig(level=logging.DEBUG,filename='atom-seller.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

logging.info("Starting atom-seller")


amount_sold = 0.0
num_orders = 0
open_orders_total = 0.0
exch = None
selected_exchange = settings.EXCHANGE


# Read in static data if available
try:
    with open('atom-seller-data.json') as infile:
        data = json.load(infile)
        amount_sold = data['amount_sold']
        num_orders = data['num_orders']
except FileNotFoundError:
    logging.info("No json file")


# Check which exchange to use
if selected_exchange == 'POLO':
    exch = Poloniex(private.API_KEY[selected_exchange], private.API_SECRET[selected_exchange], settings.CURRENCY_PAIR, settings.TICKER)
elif selected_exchange == 'KRAKEN':
    exch = Kraken(private.API_KEY[selected_exchange], private.API_SECRET[selected_exchange], settings.CURRENCY_PAIR, settings.TICKER)

    
# Get price inside spread
def price_inside_spread():
    highest_bid = exch.get_highest_bid()
    lowest_ask = exch.get_lowest_ask()

    spread = lowest_ask - highest_bid

    order_price = highest_bid + (spread / 2)

    return order_price


# Work out sell interval for orders
def order_velocity():
    day = 24 * 60 * 60
    price = price_inside_spread()

    min_order = settings.MIN_ORDER / price
    num_orders = settings.TARGET_VOLUME_DAY / min_order
    velocity = day / num_orders

    return velocity


# Place limit order inside spread
def place_order():
    global num_orders, amount_sold

    price = price_inside_spread()

    # Determine min order
    min_order = settings.MIN_ORDER / price

    # if balance greater than .5 and if price that you're selling at is greater than the min price that I've set in USD
    if exch.get_last_price(settings.CURRENCY_PAIR) * exch.get_usd_price() > settings.MIN_PRICE and float(exch.get_balance(settings.SELLING)) > 0.5:
        exch.sell(settings.CURRENCY_PAIR, price, min_order)

        num_orders += 1
        amount_sold += min_order


def save_data():
    data = {}
    data['amount_sold'] = amount_sold
    data['num_orders'] = num_orders

    with open('atom-seller-data.json', 'w') as outfile:
        json.dump(data, outfile)


# Live CLI updates
def cli_update():
    btc_price = float(exch.get_usd_price()) #TODO make variable name currency agnostic
    btc_balance = exch.get_balance(settings.TICKER) #TODO make variable name currency agnostic
    atom_balance = float(exch.get_balance(settings.SELLING)) #TODO make variable name currency agnostic
    atom_price = float(exch.get_last_price(settings.CURRENCY_PAIR)) #TODO make variable name currency agnostic

    open_orders = exch.get_open_orders()
    open_orders_total = exch.get_open_orders_total(settings.CURRENCY_PAIR)
    order_vel = order_velocity()

    if private.OS == 'LINUX':
        system('clear')
    else:
        system('cls')

    print("Atom Seller")
    print(" ")
    print(f"Current prices: BTC ${round(btc_price, 2)} USD :::: ATOM ${round(atom_price * btc_price, 2)} USD")
    print(" ")
    print(f"Target of {settings.TARGET_VOLUME_DAY} ATOM per day, with minimum price of ${settings.MIN_PRICE} USD, and sell interval of {round(order_vel / 60)} minutes and {round(order_vel % 60)} seconds.")
    print(" ")
    print(f"Current BTC balance is {round(btc_balance, 5)} (${round(btc_balance * btc_price, 2)} USD), and ATOM balance is {round(atom_balance, 5)} (${round(atom_balance * atom_price * btc_price, 2)} USD)")
    print(" ")
    print(f"Number of orders executed: {num_orders}")
    print(f"Total ATOM sold: {round(amount_sold, 8)}")
    print(f"Number of open orders: {open_orders}")
    print(f"Total ATOM in open orders: {open_orders_total}")
    

def run_updates():
    cli_update()
    save_data()


def thread_one():
    threading.Timer(10, thread_one).start()
    run_updates()


def thread_two():
    time.sleep(5)
    place_order()
    threading.Timer(order_velocity(), thread_two).start()


thread_one()
thread_two()