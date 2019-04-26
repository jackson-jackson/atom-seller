import poloniex
import private
import settings

polo = settings.POLO

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

class Ethereum:
    @staticmethod
    def balance():
        balance = polo.returnBalances()
        balance = float(balance['ETH'])

        return balance

    @staticmethod
    def price():
        price = get_last_price('USDT_ETH')

        return price