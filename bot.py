from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("6368579330:AAFfXOvMLYDdKHkSsw9hvQ512klIpQxrBmg")
CHANNEL = os.getenv("Learndotfar")  # مثلاً @yourchannel

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def is_subscribed(bot, user_id):
    try:
        member = bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    if is_subscribed(context.bot, user.id):
        update.message.reply_text("✅ عضو هستی! خوش اومدی.")
    else:
        keyboard = [
            [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL[1:]}")],
            [InlineKeyboardButton("عضو شدم ✅", callback_data='check')]
        ]
        update.message.reply_text(
            "برای استفاده از ربات باید عضو کانال بشی:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def check_join(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    if is_subscribed(context.bot, user_id):
        query.edit_message_text("✅ عضویت تأیید شد! حالا از ربات استفاده کن.")
    else:
        query.answer("❌ هنوز عضو نشدی!", show_alert=True)

def main():
    keep_alive()
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(check_join))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
