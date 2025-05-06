import ccxt
import os

def get_price_binance(symbol="BTC/USDT"):
    return ccxt.binance().fetch_ticker(symbol)['ask'], ccxt.binance().fetch_ticker(symbol)['bid']

def get_price_coinbase(symbol="BTC/USD"):
    return ccxt.coinbase().fetch_ticker(symbol)['ask'], ccxt.coinbase().fetch_ticker(symbol)['bid']

def get_price_kraken(symbol="BTC/USD"):
    return ccxt.kraken().fetch_ticker(symbol)['ask'], ccxt.kraken().fetch_ticker(symbol)['bid']

# Add similar for Bybit, OKX, KuCoin, Bitfinex, Bitstamp, Huobi, Gate.io

