
import ccxt
import os

def get_price_binance(symbol="BTC/USDT"):
    exchange = ccxt.binance({
        'apiKey': os.getenv('BINANCE_API_KEY'),
        'secret': os.getenv('BINANCE_SECRET')
    })
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']

def get_price_coinbase(symbol="BTC/USD"):
    exchange = ccxt.coinbase({
        'apiKey': os.getenv('COINBASE_API_KEY'),
        'secret': os.getenv('COINBASE_SECRET')
    })
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']

def get_price_kraken(symbol="BTC/USD"):
    exchange = ccxt.kraken({
        'apiKey': os.getenv('KRAKEN_API_KEY'),
        'secret': os.getenv('KRAKEN_SECRET')
    })
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']

def get_price_bybit(symbol="BTC/USDT"):
    exchange = ccxt.bybit({
        'apiKey': os.getenv('BYBIT_API_KEY'),
        'secret': os.getenv('BYBIT_SECRET')
    })
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']

def get_price_okx(symbol="BTC/USDT"):
    exchange = ccxt.okx({
        'apiKey': os.getenv('OKX_API_KEY'),
        'secret': os.getenv('OKX_SECRET')
    })
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']

def get_price_kucoin(symbol="BTC/USDT"):
    exchange = ccxt.kucoin({
        'apiKey': os.getenv('KUCOIN_API_KEY'),
        'secret': os.getenv('KUCOIN_SECRET')
    })
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']

def get_price_bitfinex(symbol="BTC/USDT"):
    exchange = ccxt.bitfinex({
        'apiKey': os.getenv('BITFINEX_API_KEY'),
        'secret': os.getenv('BITFINEX_SECRET')
    })
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']

def get_price_bitstamp(symbol="BTC/USD"):
    exchange = ccxt.bitstamp({
        'apiKey': os.getenv('BITSTAMP_API_KEY'),
        'secret': os.getenv('BITSTAMP_SECRET')
    })
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']

def get_price_huobi(symbol="BTC/USDT"):
    exchange = ccxt.huobi({
        'apiKey': os.getenv('HUOBI_API_KEY'),
        'secret': os.getenv('HUOBI_SECRET')
    })
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']

def get_price_gateio(symbol="BTC/USDT"):
    exchange = ccxt.gateio({
        'apiKey': os.getenv('GATEIO_API_KEY'),
        'secret': os.getenv('GATEIO_SECRET')
    })
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']
