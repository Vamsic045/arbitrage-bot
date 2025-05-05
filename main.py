from config import ALERT_ON, AUTO_TRADE

if profit > threshold:
    if ALERT_ON:
        send_telegram_alert(...)
    if AUTO_TRADE:
        place_order(...)
from telegram_alert import send_telegram_alert

# Arbitrage opportunity వచినప్పుడు:
profit = 2.4  # ఉదాహరణకు
if profit >= 1.5:
    send_telegram_alert(f"🚀 Arbitrage Opportunity Found!\nProfit: {profit}%")

