import os
import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from settings import TELEGRAM_TOKEN, OWNER_CHAT_ID, stocks

SUGGESTIONS_PATH = "suggestions_log.json"
logging.basicConfig(level=logging.INFO)

def load_suggestions():
    try:
        with open(SUGGESTIONS_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

def save_suggestions(data):
    with open(SUGGESTIONS_PATH, "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔒 מאזין פעיל. פקודות: /approve /reject /reset_suggestions")

async def reset_suggestions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != OWNER_CHAT_ID:
        return
    save_suggestions({})
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text="🧼 ההצעות אופסו.")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    suggestions = load_suggestions()

    if data.startswith("approve:"):
        _, symbol, field, value = data.split(":")
        if symbol in stocks and field in ["low", "high"]:
            stocks[symbol][field] = float(value)
            if symbol in suggestions and field in suggestions[symbol]:
                del suggestions[symbol][field]
                if not suggestions[symbol]:
                    del suggestions[symbol]
            save_suggestions(suggestions)
            await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=f"✅ אושר: עודכן {field} של {symbol} ל־{value}")

    elif data.startswith("reject:"):
        _, symbol, field = data.split(":")
        if symbol in suggestions and field in suggestions[symbol]:
            del suggestions[symbol][field]
            if not suggestions[symbol]:
                del suggestions[symbol]
            save_suggestions(suggestions)
            await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=f"🚫 נדחה: {field} של {symbol} לא עודכן")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset_suggestions", reset_suggestions))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()

if __name__ == "__main__":
    main()
