from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_ai(text):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [{"text": text}]
            }
        ]
    }

    try:
        r = requests.post(url, json=payload, timeout=20)
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "⚠️ خطأ في الذكاء الاصطناعي"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 البوت يعمل الآن")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = ask_ai(update.message.text)
    await update.message.reply_text(reply)

app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
