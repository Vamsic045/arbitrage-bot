from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from calc_profit import calculate_arbitrage
from config import TOP_100_COINS
from trusted_exchanges import get_top_100_trusted_exchanges

EXCHANGES = get_top_100_trusted_exchanges()
YOUR_CHAT_ID = "YOUR_CHAT_ID_HERE"  # Replace with your actual Telegram chat ID

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🚀 Welcome to Arbitrage Bot! You’ll receive updates every minute.")

def send_opportunities(context: CallbackContext):
    opportunities = []
    for symbol in TOP_100_COINS:
        for ex1 in EXCHANGES:
            for ex2 in EXCHANGES:
                if ex1 == ex2:
                    continue
                result = calculate_arbitrage(symbol, ex1, ex2)
                if result:
                    opportunities.append(result)
    opportunities.sort(key=lambda x: x['profit'], reverse=True)
    message = "\n".join([
        f"{o['symbol']} | Buy: {o['buy_from']} @ {o['buy_price']} → Sell: {o['sell_to']} @ {o['sell_price']} | Profit: {round(o['profit'], 2)}"
        for o in opportunities[:5]
    ])
    context.bot.send_message(chat_id=context.job.context, text=message)

def setup_bot():
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.job_queue.run_repeating(send_opportunities, interval=60, first=10, context=YOUR_CHAT_ID)
    updater.start_polling()
    updater.idle()
