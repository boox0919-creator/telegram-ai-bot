import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_ai(text):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": text}]}]}

    try:
        r = requests.post(url, json=payload, timeout=20)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "⚠️ خطأ في الذكاء الاصطناعي"

def start(update, context):
    update.message.reply_text("🤖 البوت يعمل الآن")

def handle(update, context):
    reply = ask_ai(update.message.text)
    update.message.reply_text(reply)

def main():
    if not TELEGRAM_TOKEN:
        print("Missing TELEGRAM_TOKEN")
        return

    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))

    print("Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
