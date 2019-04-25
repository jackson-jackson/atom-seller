import poloniex
import private

polo = poloniex.Poloniex(private.API_KEY,private.API_SECRET)

def get_last_price(currency_pair):
    tickers = polo.returnTicker()
    last_price = float(tickers[currency_pair]['last'])
    
    return last_price


class Bitcoin:
    @staticmethod
    def balance():
        balance = polo.returnBalances()
        balance = float(balance['BTC'])

        return balance

    @staticmethod
    def price():
        price = get_last_price('USDT_BTC')

        return price
        

class Atom:
    @staticmethod
    def balance():
        balance = polo.returnBalances()
        balance = float(balance['ATOM'])

        return balance

    @staticmethod
    def price():
        price = get_last_price('BTC_ATOM')

        return price