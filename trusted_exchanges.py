import ccxt

def get_top_100_trusted_exchanges():
    exchange_list = []
    for ex_id in ccxt.exchanges:
        try:
            ex = getattr(ccxt, ex_id)()
            if ex.has.get('fetchOrderBook') and ex.has.get('fetchTicker'):
                exchange_list.append(ex_id)
        except Exception:
            continue
    return exchange_list[:100]
