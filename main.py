import poloniex
import private
import math
import time
import json

polo = poloniex.Poloniex(private.API_KEY,private.API_SECRET)
balances = polo.returnBalances()
min_order_btc = 0.001 # This is Polo's minimum order size 
one_week = 604800

token = 'ATOM'
currency_pair = 'BTC_ATOM'


# Check token balance
def check_balance(token):
    if float(balances[token]) > 0.00001:
        return float(balances[token])


# Determine number or orders based on the minimum order size
def number_of_orders(token):
    if float(check_balance(token)) > min_order_btc:
        number_of_orders = math.floor(check_balance(token) / min_order_btc)
        return number_of_orders


# Determine the sell interval, in seconds, required to sell entire balance over one week
sell_interval = math.floor(one_week / number_of_orders(token))


# Get average price of currency pair
def get_average_price(currency_pair):
    
    orderbook = polo.returnOrderBook(currency_pair, depth=10)
    
    sum_price = 0

    for ask in orderbook['asks']:
       sum_price += float(ask[0])

    return round(sum_price / len(orderbook['asks']), 8)


# Sell token balance over 7 days using the minimum order size
def sell_token(token):
    balance = check_balance(token)
    print(f"Balance: {balance}")
    orders = number_of_orders(token)
    print(f"Number of Orders: {orders}")
    count = 0
    while count <= orders:
        price = get_average_price(currency_pair)
        # polo.buy(currency_pair, price, min_order_btc)
        print(f"Order {count} of {orders}")
        count += 1
        print(f"Sleeping for {time.sleep(sell_interval)}")
        time.sleep(sell_interval)

sell_token(token)

