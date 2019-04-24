import poloniex
import private
import math
import time

polo = poloniex.Poloniex(private.API_KEY,private.API_SECRET)

min_order = .15 #TODO make this based on min btc order size of .0001
time_to_sell = 350 #TODO use a better variable name

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


# Sell token balance over 7 days using the minimum order size
def sell_token(token):
    token_balance = check_balance(token)
    print(f"Balance: {token_balance}")
    orders = number_of_orders(token)
    print(f"Number of Orders: {orders}")
    count = 0
    # Determine the sell interval, in seconds, required to sell entire balance over one week
    sell_interval = math.floor(time_to_sell / number_of_orders(token))
    while count < 2:
        price = get_average_price(currency_pair)
        polo.sell(currency_pair, price, min_order) # DANGER DANGER DANGER
        print(f"Order {count + 1} of {orders}")
        count += 1
        print(f"Sleeping for {sell_interval}")
        time.sleep(sell_interval)

        #TODO add error handling

sell_token(token)

