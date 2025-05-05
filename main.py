from config import ALERT_ON, AUTO_TRADE

if profit > threshold:
    if ALERT_ON:
        send_telegram_alert(...)
    if AUTO_TRADE:
        place_order(...)

