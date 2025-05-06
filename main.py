
from exchanges import *
from telegram_alert import send_telegram_alert

# Add exchanges to check here
exchanges = {
    "Binance": get_price_binance(),
    "Coinbase": get_price_coinbase(),
    "Kraken": get_price_kraken(),
    "Bybit": get_price_bybit(),
    "OKX": get_price_okx(),
    "KuCoin": get_price_kucoin(),
    "Bitfinex": get_price_bitfinex(),
    "Bitstamp": get_price_bitstamp(),
    "Huobi": get_price_huobi(),
    "Gate.io": get_price_gateio(),
}

buy_exchange = min(exchanges, key=lambda x: exchanges[x][0])
sell_exchange = max(exchanges, key=lambda x: exchanges[x][1])

buy_price = exchanges[buy_exchange][0]
sell_price = exchanges[sell_exchange][1]

profit_percent = (sell_price - buy_price) / buy_price * 100

message = f""" 
🚨 <b>Arbitrage Opportunity</b> 🚨

Buy from: <b>{buy_exchange}</b> at <code>{buy_price}</code>
Sell on: <b>{sell_exchange}</b> at <code>{sell_price}</code>

💰 Estimated Profit: <b>{profit_percent:.2f}%</b>
"""

print(message)
send_telegram_alert(message)
