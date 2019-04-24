import poloniex
import private
import math
import time

polo = poloniex.Poloniex(private.API_KEY,private.API_SECRET)

min_order = .25 #TODO make this based on min btc order size of .0001

#               D   H   M   S
time_to_sell =  1 * 1 * 5 * 60

token = 'ATOM'
currency_pair = 'BTC_ATOM'


# Check token balance
def check_balance(token):
    balances = polo.returnBalances()
    if float(balances[token]) > 0.00001:
        return float(balances[token])


# Determine number or orders based on the minimum order size
def number_of_orders(token):
    token_balance = check_balance(token)    
    if token_balance > min_order:
        number_of_orders = math.floor(token_balance / min_order)
        return number_of_orders #TODO Optimize by returning token balance as well
    return 0


# Get average price of currency pair
def get_average_price(currency_pair):
    
    orderbook = polo.returnOrderBook(currency_pair, depth=5)
    
    sum_price = 0

    for ask in orderbook['bids']:
       sum_price += float(ask[0])

    return round(sum_price / len(orderbook['bids']), 8)


# Sell token balance over time_to_sell using the minimum order size
def sell_token(token):
    token_balance = check_balance(token)
    print(f"Balance: {token_balance}")
    orders = number_of_orders(token)
    print(f"Number of Orders: {orders}")
    count = 0
    # Determine the sell interval, in seconds, required to sell entire balance over one week
    sell_interval = time_to_sell / orders
    print(f"Sell Interval: {round(sell_interval)}")
    while count < 5:
        price = get_average_price(currency_pair)
        polo.sell(currency_pair, price, min_order) # DANGER DANGER DANGER
        print(f"Order {count + 1} of {orders}")
        count += 1
        print(f"Sleeping for {round(sell_interval)}")
        time.sleep(sell_interval)
    print("Done")

        #TODO add error handling
        #TODO add timestamping


sell_token(token)

