import requests
import datetime
import csv
from settings import TELEGRAM_TOKEN, CHAT_IDS
from core.utils import calculate_buy_amount

def send_telegram(msg, chat_id=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    target_ids = [chat_id] if chat_id else CHAT_IDS

    for cid in target_ids:
        try:
            requests.post(url, data={"chat_id": cid, "text": msg})
        except Exception as e:
            print(f"[ERROR] Failed to send message to {cid}: {e}")

def log_to_csv(symbol, price, action):
    with open("signals_log.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now().isoformat(), symbol, price, action])


def notify(symbol, price, rating, rsi, action, news, score, reasons):
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    msg = f"📌 {symbol} – ${price}\n"
    msg += f"⏰ {now}\n"

    msg += f"\n📊 אינדיקטורים:\n"
    msg += f"• RSI: {rsi if rsi else 'N/A'}\n"
    msg += f"• אנליסטים – BUY: {rating.get('buy', 0)} | SELL: {rating.get('sell', 0)}\n"

    if reasons:
        msg += "\n📊 סיבות לאיתות:\n"
        for reason in reasons:
            msg += f"• {reason}\n"

    msg += f"\n🔔 ציון AI: {score}/100"
    try:
        amount = calculate_buy_amount(price)
        units = int(amount // price)
        msg += f"\n💰 הצעה: לקנות בכ־${amount} (~{units} יח')"
    except:
        pass
    msg += f"\n📢 {action}"

    send_telegram(msg)
    log_to_csv(symbol, price, action)
def send_alert(symbol, price, score, reason="איתות AI"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"📡 {reason} 📡\n"
    msg += f"🔹 מניה: {symbol}\n"
    msg += f"💵 שער: ${price}\n"
    msg += f"🧠 ציון AI: {score}/100\n"
    msg += f"⏰ {now}"
    send_telegram(msg)
    log_to_csv(symbol, price, reason)

from settings import OWNER_CHAT_ID, TELEGRAM_TOKEN
import requests

def send_candidate_to_telegram(symbol, price, score):
    message = (
        f"📈 מועמדת חדשה: *{symbol}*\n"
        f"מחיר נוכחי: ${price}\n"
        f"ציון AI: *{score}*\n\n"
        "תרצה להוסיף אותה לתיק שלך?"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": OWNER_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [[
                {
                    "text": "➕ הוסף לתיק",
                    "callback_data": f"add:{symbol}"
                }
            ]]
        }
    }

    try:
        requests.post(url, json=data)
    except Exception as e:
        print(f"[ERROR] Failed to send candidate to Telegram: {e}")
