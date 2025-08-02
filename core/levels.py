
import json
from settings import TELEGRAM_TOKEN, OWNER_CHAT_ID
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def send_approval_request(symbol, field, value):
    msg = f"🛠️ הצעה לעדכון {field} עבור {symbol}: {value}"
    buttons = [[
        InlineKeyboardButton("✅ אשר", callback_data=f"approve:{symbol}:{field}:{value}"),
        InlineKeyboardButton("❌ דחה", callback_data=f"reject:{symbol}:{field}")
    ]]
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": OWNER_CHAT_ID,
        "text": msg,
        "reply_markup": InlineKeyboardMarkup(buttons).to_dict()
    }
    requests.post(url, json=payload)

import json
import os
from core.notifier import send_telegram

SUGGESTIONS_PATH = "suggestions_log.json"
MIN_DIFF_LOW = 300.0    # פער מינימלי לעדכון LOW
MIN_DIFF_HIGH = 300.0   # פער מינימלי לעדכון HIGH

def load_suggestions():
    if os.path.exists(SUGGESTIONS_PATH):
        with open(SUGGESTIONS_PATH, "r") as f:
            return json.load(f)
    return {}

def save_suggestions(suggestions):
    with open(SUGGESTIONS_PATH, "w") as f:
        json.dump(suggestions, f)

def suggest_level_updates(stocks):
    suggestions = load_suggestions()
    updated = False

    for symbol, data in stocks.items():
        if len(data["prices"]) < 10:
            continue

        lows_broken = [p for p in data["prices"] if p < data["low"]]
        highs_broken = [p for p in data["prices"] if p > data["high"]]

        msg_parts = []
        symbol_log = suggestions.get(symbol, {})

        # LOW
        if len(lows_broken) >= 3:
            suggested_low = round(sum(lows_broken[-3:]) / 3, 2)
            if abs(data["low"] - suggested_low) >= MIN_DIFF_LOW and symbol_log.get("low") != suggested_low:
                msg_parts.append(f"🔻 הצעה: עדכון low מ־{data['low']} ל־{suggested_low}")
                symbol_log["low"] = suggested_low
                updated = True

        # HIGH
        if len(highs_broken) >= 3:
            suggested_high = round(sum(highs_broken[-3:]) / 3, 2)
            if abs(data["high"] - suggested_high) >= MIN_DIFF_HIGH and symbol_log.get("high") != suggested_high:
                msg_parts.append(f"🔺 הצעה: עדכון high מ־{data['high']} ל־{suggested_high}")
                symbol_log["high"] = suggested_high
                updated = True

        if msg_parts:
            send_telegram(f"📊 {symbol} – המלצות עדכון:\n" + "\n".join(msg_parts))

        suggestions[symbol] = symbol_log

    if updated:
        save_suggestions(suggestions)
