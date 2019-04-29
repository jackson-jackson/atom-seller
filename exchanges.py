import poloniex
import krakenex
import settings
import private

selected_exchange = settings.EXCHANGE


class Exchange:
    pass


class Poloniex(Exchange):
    def __init__(self, key, secret, currency_pair, ticker):
        if not currency_pair:
            raise TypeError("currency_pair is required")

        self.polo = poloniex.Poloniex(key, secret)
        self.currency_pair = currency_pair
        self.ticker = ticker
    

    # Get lowest ask price on orderbook
    def get_lowest_ask(self):
        tickers = self.polo.returnTicker()
        lowest_ask = tickers[self.currency_pair]['lowestAsk']

        return float(lowest_ask)

    
    # Get highest bid price on orderbook
    def get_highest_bid(self):
        tickers = self.polo.returnTicker()
        highest_bid = tickers[self.currency_pair]['highestBid']

        return float(highest_bid)


    # Get total number of currency in open orders
    def get_open_orders(self):
        orders = self.polo.returnOpenOrders(self.currency_pair)
        
        open_orders = []
        
        for order in orders:
            open_orders.append(float(order['total']))

        return len(open_orders)


    # Get sum total of all open orders for a given currency
    def get_open_orders_total(self, currency_pair):
        orders = self.polo.returnOpenOrders(currency_pair)
        open_orders = []

        for order in orders:
            open_orders.append(float(order['total']))
        return round(sum(open_orders), 8)


    # Get currency_pair's last price
    def get_last_price(self, currency_pair):
        tickers = self.polo.returnTicker()
        last_price = tickers[self.currency_pair]['last']
    
        return float(last_price)


    # Return ticker balance
    def get_balance(self, ticker):
        balance = self.polo.returnBalances()
        balance = balance[ticker]

        return float(balance)


    # Return currency_pair price in USD
    def get_usd_price(self):
        tickers = self.polo.returnTicker()
        last_price = tickers['USDT_BTC']['last']
    
        return float(last_price)


    # Sell 
    def sell(self, currency_pair, price, min_order):
        self.polo.sell(currency_pair, price, min_order)



class Kraken(Exchange):
    def __init__(self, key, secret, currency_pair, ticker):
        if not currency_pair:
            raise TypeError("currency_pair is required")

        self.kraken = krakenex.API(key, secret)
        self.currency_pair = currency_pair
        self.ticker = ticker
    

    # Get lowest ask price on orderbook
    def get_lowest_ask(self):
        ticker = self.kraken.query_public('Ticker', {'pair': self.currency_pair})
        lowest_ask = ticker['result']['ATOMXBT']['a'][0]

        return float(lowest_ask)


    # Get highest ask price on orderbook
    def get_highest_bid(self):
        ticker = self.kraken.query_public('Ticker', {'pair': self.currency_pair})
        highest_bid = ticker['result']['ATOMXBT']['b'][0]

        return float(highest_bid)

    
    # Get total number of currency in open orders #TODO Test this with orders on Kraken
    def get_open_orders(self):
        orders = self.kraken.query_private('OpenOrders', {'trades': 'status'})
    
        # open_orders = []
        
        # for order in orders:
        #     open_orders.append(float(order['total']))
    
        return orders