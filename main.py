import poloniex
import private
import math
import time

polo = poloniex.Poloniex(private.API_KEY,private.API_SECRET)
balances = polo.returnBalances()

min_order = .15 # TODO make this based on min btc order size of .0001
one_week = 604800 #TODO use a better variable name

token = 'ATOM'
currency_pair = 'BTC_ATOM'


# Check token balance
def check_balance(token):
    if float(balances[token]) > 0.00001:
        return float(balances[token])


# Determine number or orders based on the minimum order size
def number_of_orders(token):
    if float(check_balance(token)) > min_order:
        number_of_orders = math.floor(check_balance(token) / min_order)
        return number_of_orders


# Get average price of currency pair
def get_average_price(currency_pair):
    
    orderbook = polo.returnOrderBook(currency_pair, depth=5)
    
    sum_price = 0

    for ask in orderbook['bids']:
       sum_price += float(ask[0])

    return round(sum_price / len(orderbook['bids']), 8)


# Sell token balance over 7 days using the minimum order size
def sell_token(token):
    balance = check_balance(token)
    print(f"Balance: {balance}")
    orders = number_of_orders(token) + 1
    print(f"Number of Orders: {orders}")
    count = 1
    # Determine the sell interval, in seconds, required to sell entire balance over one week
    sell_interval = 10
    # sell_interval = math.floor(one_week / number_of_orders(token))
    print(f"Sell Interval in Seconds: {sell_interval}")
    while count <= 2:
        price = get_average_price(currency_pair)
        polo.sell(currency_pair, price, min_order) # DANGER DANGER DANGER
        print(f"Order {count} of {orders}")
        count += 1
        print(f"Sleeping for {time.sleep(sell_interval)}")
        time.sleep(sell_interval)

        #TODO add error handling

sell_token(token)

