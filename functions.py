import poloniex
import private
import settings


polo = settings.POLO
currency_pair = 'BTC_ATOM'
price = 0.01000000
amount = 1


def place_orders():
    polo.sell(currency_pair, price, amount)
    polo.sell(currency_pair, price + .001, amount)


def open_orders():
    orders = polo.returnOpenOrders('BTC_ATOM')
    open_orders = []

    for order in orders:
        open_orders.append(order['orderNumber'])
    return open_orders


def cancel_orders():
    for order in open_orders():
        polo.cancelOrder(order)


def price_inside_spread():
        tickers = polo.returnTicker()
        highest_bid = float(tickers[currency_pair]['highestBid'])
        lowest_ask = float(tickers[currency_pair]['lowestAsk'])
        
        spread = lowest_ask - highest_bid

        order_price = highest_bid + (spread / 2)

        return round(order_price, 8)


def get_open_orders_total():
    orders = polo.returnOpenOrders('BTC_ATOM')
    open_orders = []

    for order in orders:
        open_orders.append(float(order['total']))
    return round(sum(open_orders), 8)


tickers = polo.returnTicker()
tickers['USDT_BTC']['last']