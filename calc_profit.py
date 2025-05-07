from fetch_data import get_order_book

def calculate_arbitrage(symbol, exA, exB):
    bookA = get_order_book(exA, symbol)
    bookB = get_order_book(exB, symbol)

    if not bookA['ask'] or not bookB['bid']:
        return None

    profit = bookB['bid'] - bookA['ask']
    return {
        'symbol': symbol,
        'buy_from': exA,
        'sell_to': exB,
        'buy_price': bookA['ask'],
        'sell_price': bookB['bid'],
        'profit': profit
    } if profit > 0 else None
