import ccxt, time, requests

# Initialize trusted exchanges (15)
exchanges = {
    'Binance': ccxt.binance(),
    'Kraken': ccxt.kraken(),
    'KuCoin': ccxt.kucoin(),
    'Gate.io': ccxt.gateio(),
    'Bitfinex': ccxt.bitfinex(),
    'OKX': ccxt.okx(),
    'Bybit': ccxt.bybit(),
    'Bitstamp': ccxt.bitstamp(),
    'Poloniex': ccxt.poloniex(),
    'MEXC': ccxt.mexc(),
    'Coinbase': ccxt.coinbase(),
    'Bittrex': ccxt.bittrex(),
    'LBank': ccxt.lbank(),
    'XT.COM': ccxt.xt(),
    'Bitget': ccxt.bitget()
}

# Telegram bot config
bot_token = '7802388978:AAGs1K461PsA6CgzqXaucWj5HkpCZJfApyI'
chat_id = '6738389946'

def fetch_usdt_to_inr():
    try:
        r = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=USDTINR')
        return float(r.json()['price'])
    except:
        return 83.0  # fallback rate

def fetch_order_prices(exchange, symbol):
    try:
        ob = exchange.fetch_order_book(symbol)
        bid = ob['bids'][0][0] if ob['bids'] else None
        ask = ob['asks'][0][0] if ob['asks'] else None
        return bid, ask
    except:
        return None, None

def send_telegram(message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    requests.post(url, data={'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'})

while True:
    usdt_inr = fetch_usdt_to_inr()
    coins = ['1INCH', 'ACH', 'AGIX', 'GALA', 'DENT', 'TRX', 'VET', 'COTI', 'WAVES', 'WRX',
             'XRP', 'SHIB', 'HBAR', 'BTT', 'DOGE', 'ICP', 'RUNE', 'SAND', 'MANA', 'MASK',
             'ZIL', 'ENS', 'ANKR', 'XLM', 'CTSI', 'CELR', 'FET', 'CVC', 'STORJ', 'ARPA',
             'OMG', 'BAND', 'NKN', 'ALGO', 'FLUX', 'XNO', 'CHZ', 'BICO', 'BLUR', 'REQ',
             'SKL', 'HIGH', 'RLC', 'OCEAN', 'GLM', 'DGB', 'TRB', 'SPELL', 'ILV', 'PLA']

    opportunities = []

    for coin in coins:
        for buy_ex_name, buy_ex in exchanges.items():
            for sell_ex_name, sell_ex in exchanges.items():
                if buy_ex_name == sell_ex_name:
                    continue
                try:
                    buy_bid, buy_ask = fetch_order_prices(buy_ex, f'{coin}/USDT')
                    sell_bid, sell_ask = fetch_order_prices(sell_ex, f'{coin}/USDT')
                    if not buy_ask or not sell_bid:
                        continue
                    if buy_ask * usdt_inr < 10 or buy_ask * usdt_inr > 1000:
                        continue
                    # Check withdrawal and deposit
                    cur1 = buy_ex.fetch_currencies().get(coin, {})
                    cur2 = sell_ex.fetch_currencies().get(coin, {})
                    can_withdraw = cur1.get('withdraw', False)
                    can_deposit = cur2.get('deposit', False)
                    fee = cur1.get('fee', 0)
                    if not (can_withdraw and can_deposit):
                        continue
                    # Calculate profit
                    spend = 100000  # ₹
                    coins_bought = spend / (buy_ask * usdt_inr)
                    net_coins = coins_bought - fee
                    revenue = net_coins * (sell_bid * usdt_inr)
                    profit = revenue - spend
                    if profit > 0:
                        opportunities.append({
                            'coin': coin,
                            'buy_ex': buy_ex_name,
                            'sell_ex': sell_ex_name,
                            'buy_price': buy_ask * usdt_inr,
                            'sell_price': sell_bid * usdt_inr,
                            'profit': profit,
                            'fee': fee,
                            'dep': '✅' if can_deposit else '❌',
                            'with': '✅' if can_withdraw else '❌'
                        })
                except Exception:
                    continue

    # Send top 10 profitable
    top = sorted(opportunities, key=lambda x: x['profit'], reverse=True)[:10]
    for o in top:
        msg = (f"🪙 *{o['coin']}* Arbitrage\n"
               f"Buy @ {o['buy_ex']}: ₹{o['buy_price']:.2f}\n"
               f"Sell @ {o['sell_ex']}: ₹{o['sell_price']:.2f}\n"
               f"💰 Profit: ₹{o['profit']:.2f}\n"
               f"📤 Withdraw: {o['with']} | 📥 Deposit: {o['dep']}\n"
               f"💸 Withdraw Fee: {o['fee']} {o['coin']}")
        send_telegram(msg)
    time.sleep(60)
