from telegram_alert import send_telegram_alert
import os
from dotenv import load_dotenv

load_dotenv()

ALERT_ON = os.getenv("ALERT_ON", "true").lower() == "true"
AUTO_TRADE = os.getenv("AUTO_TRADE", "false").lower() == "true"

# Example logic: you can replace this with real arbitrage logic later
profit = 2.5  # Example profit percentage

if profit >= 1.5:
    if ALERT_ON:
        send_telegram_alert(f"🚀 Arbitrage Opportunity Found!\nProfit: {profit}%")
    if AUTO_TRADE:
        print("Auto trading enabled (this is where order code would go).")
else:
    print("No profitable opportunity found.")
