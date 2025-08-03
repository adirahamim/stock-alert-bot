
import os
import json
import logging
import asyncio
import subprocess
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from settings import TELEGRAM_TOKEN, OWNER_CHAT_ID, stocks
from core.fetcher import get_price, get_ema
from core.settings_updater import add_stock_to_settings

logging.basicConfig(level=logging.INFO)
SUGGESTIONS_PATH = "suggestions_log.json"

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
    await update.message.reply_text("🔒 מאזין פעיל. פקודות: /explore /update_prices /reset_prices /send_report /add_stock /snapshot")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if not data.startswith("addstock:"):
        return
    _, symbol = data.split(":")
    add_stock_to_settings(symbol)
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=f"✅ {symbol} נוסף לתיק ב־settings.py")

async def explore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != OWNER_CHAT_ID:
        return
    try:
        proc = await asyncio.create_subprocess_exec("python", "explorer.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = await proc.communicate()
        result = out.decode() + err.decode()
        await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=result or "⚠️ לא התקבל פלט.")
    except Exception as e:
        await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=f"⚠️ שגיאה: {e}")

async def update_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != OWNER_CHAT_ID:
        return
    try:
        proc = await asyncio.create_subprocess_exec("python", "update_levels.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = await proc.communicate()
        result = out.decode() + err.decode()
        await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=result or "⚠️ לא התקבל פלט.")
    except Exception as e:
        await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=f"⚠️ שגיאה: {e}")

async def reset_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != OWNER_CHAT_ID:
        return
    for sym in stocks:
        stocks[sym]["low"] = None
        stocks[sym]["high"] = None
        stocks[sym]["buy_price"] = None
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text="🧼 טווחי מחירים אופסו.")

async def send_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != OWNER_CHAT_ID:
        return
    lines = ["📊 דו'ח תיק מניות:"]
    for sym, data in stocks.items():
        price = get_price(sym)
        status = "⛔" if price is None else f"{price}$"
        lines.append(f"{sym}: {status}")
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text="\n".join(lines))

async def add_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != OWNER_CHAT_ID:
        return
    args = context.args
    if not args:
        await context.bot.send_message(chat_id=OWNER_CHAT_ID, text="❗ השתמש ב־/add_stock SYMBOL")
        return
    symbol = args[0].upper()
    add_stock_to_settings(symbol)
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=f"✅ {symbol} נוסף לתיק")

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != OWNER_CHAT_ID:
        return
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"settings_backup_{ts}.py"
    try:
        with open("settings.py", "r", encoding="utf-8") as f:
            content = f.read()
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)
        await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=f"🗂️ גובּה אל {fname}")
    except Exception as e:
        await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=f"⚠️ שגיאה בגיבוי: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("explore", explore))
    app.add_handler(CommandHandler("update_prices", update_prices))
    app.add_handler(CommandHandler("reset_prices", reset_prices))
    app.add_handler(CommandHandler("send_report", send_report))
    app.add_handler(CommandHandler("add_stock", add_stock))
    app.add_handler(CommandHandler("snapshot", snapshot))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()

if __name__ == "__main__":
    main()
