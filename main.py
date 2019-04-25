import poloniex
import private
import math
import time
import threading
from os import system


polo = poloniex.Poloniex(private.API_KEY,private.API_SECRET)

# Configuration
target_volume_day = 10 # Target amount of atoms that the script should sell per day
min_atom_price = 3 # Minimum atom price in USD that the script should sell at. Script will not sell below this

min_order = .25 #TODO make this based on min btc order size of .0001

token = 'ATOM'
currency_pair = 'BTC_ATOM'

btc_price = 0.0 # btc price in USD
atom_price = 0.0 # atom price in BTC
amount_sold = 0.0
num_orders = 0
btc_prices = []
atom_prices = []
atom_balance = 0.0
btc_balance = 0.0


# Update the btc and atom prices
def update_prices():
    global btc_price, atom_price

    btc_usd_book = polo.returnOrderBook('USDC_BTC', depth=3)
    btc_price = float(btc_usd_book['bids'][0][0])

    btc_prices.append(btc_price)

    btc_atom_book = polo.returnOrderBook('BTC_ATOM', depth=3)
    atom_price = float(btc_atom_book['bids'][0][0])

    atom_prices.append(btc_price * atom_price)


# Work out rate for orders
def order_velocity():
    day = 24 * 60 * 60
    num_orders = target_volume_day / min_order
    velocity = day / num_orders

    return velocity


def update_balances():
    global btc_balance, atom_balance

    balances = polo.returnBalances()
    btc_balance = balances['BTC']
    atom_balance = balances['ATOM']


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

    if atom_price > price and atom_balance > 0.5: # Above min price
        polo.sell(currency_pair, price, min_order)
        num_orders += 1
        amount_sold += min_order


def cli_update():

    system('clear')

    print(f"Atom Seller")
    print(f" ")
    print(f"Current prices: BTC {round(btc_price, 2)}  ATOM {round(atom_price * btc_price, 2)}")
    print(f" ")
    print(f"Target of {target_volume_day} atoms per day, with minimum price of {min_atom_price}, and sell interval of {order_velocity()}")
    print(f" ")
    print(f"Current BTC balance is {round(btc_balance, 2)} (${round(btc_balance * btc_price, 2)}), and ATOM balance is {round(atom_balance, 2)} (${round(atom_balance * atom_price * btc_price,2)})")
    print(f" ")
    print(f"Number of orders executed: {num_orders}")
    print(f"Total atoms sold: {amount_sold}")
    

def run_updates():
    update_prices()
    update_balances()
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