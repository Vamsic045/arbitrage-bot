from exchanges import get_price_binance, get_price_coindcx, get_price_bitget
from telegram_alert import send_telegram_alert

ask_b, bid_b = get_price_binance()
ask_c, bid_c = get_price_coindcx()
ask_g, bid_g = get_price_bitget()

message = f"""
📊 <b>Live Price Update</b>
🔹 Binance: Ask {ask_b}, Bid {bid_b}
🔹 CoinDCX: Ask {ask_c}, Bid {bid_c}
🔹 Bitget: Ask {ask_g}, Bid {bid_g}
"""

print(message)
send_telegram_alert(message)
