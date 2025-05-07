import ccxt

def get_order_book(exchange_id, symbol):
    try:
        exchange = getattr(ccxt, exchange_id)()
        order_book = exchange.fetch_order_book(symbol)
        ask = order_book['asks'][0][0] if order_book['asks'] else None
        bid = order_book['bids'][0][0] if order_book['bids'] else None
        return {'ask': ask, 'bid': bid}
    except Exception:
        return {'ask': None, 'bid': None}
