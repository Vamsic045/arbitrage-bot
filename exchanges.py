import ccxt

def get_price_binance(symbol="BTC/USDT"):
    exchange = ccxt.binance()
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']

def get_price_coindcx(symbol="BTC/USDT"):
    exchange = ccxt.coindcx()
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']

def get_price_bitget(symbol="BTC/USDT"):
    exchange = ccxt.bitget()
    ticker = exchange.fetch_ticker(symbol)
    return ticker['ask'], ticker['bid']
