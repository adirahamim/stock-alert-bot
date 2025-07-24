import os
import requests
import time
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TWELVE_API = os.getenv("TWELVE_DATA_API_KEY")
FINNHUB_API = os.getenv("FINNHUB_API_KEY")

us_timezone = pytz.timezone("America/New_York")
last_update_day = None

stocks = {
    "BBAI": {"low": 7.18, "high": 7.80, "buy_price": 7.20, "last": None},
    "SOUN": {"low": 11.40, "high": 12.00, "buy_price": 11.50, "last": None},
    "QS": {"low": 12.00, "high": 13.00, "buy_price": 12.10, "last": None},
    "REKR": {"low": 1.30, "high": 1.48, "buy_price": 1.35, "last": None},
    "RGTI": {"low": 15.50, "high": 17.00, "buy_price": 15.60, "last": None},
    "ENVX": {"low": 14.20, "high": 15.80, "buy_price": 14.30, "last": None},
    "QUIK": {"low": 6.10, "high": 6.35, "buy_price": 6.15, "last": None},
    "GDX": {"low": 52.50, "high": 54.00, "buy_price": 52.80, "last": None},
    "NVDA": {"low": 120.00, "high": 140.00, "buy_price": 131.00, "last": None},
    "TSLA": {"low": 440.00, "high": 485.00, "buy_price": 465.00, "last": None},
    "SHLD": {"low": 50.00, "high": 56.00, "buy_price": 53.50, "last": None},
    "SPY": {"low": 545.00, "high": 580.00, "buy_price": 565.00, "last": None}
}

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def get_price(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_API}"
    res = requests.get(url).json()
    return float(res["price"])

def get_news(symbol):
    url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API}"
    res = requests.get(url).json()
    return [n for n in res if symbol in n["headline"]][:1]

def get_rating(symbol):
    url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={FINNHUB_API}"
    res = requests.get(url).json()
    if res:
        rec = res[0]
        return f"🔍 מלצות אנליסטים – קנייה: {rec['buy']} | המתנה: {rec['hold']} | מכירה: {rec['sell']}"
    return "אין מלצות זמינות כרגע"

def adjust_thresholds(symbol, price):
    return {
        "low": round(price * 0.95, 2),
        "high": round(price * 1.05, 2),
        "buy_price": round(price * 0.97, 2)
    }

def evaluate(symbol, price, cfg):
    decision, reasons, amount = "המתנה", [], 0

    if price < cfg["low"]:
        decision = "קנייה"
        reasons += ["ירדה מתחת לרף תמיכה", "נראה כמו תיקון ולא שבירה"]
        amount = 500
    elif price > cfg["high"]:
        decision = "מכירה"
        reasons += ["פרצה התנגדות – רווח פוטנציאלי למימוש"]

    rec = get_rating(symbol)
    news = get_news(symbol)
    headline = news[0]["headline"] if news else "אין חדשות בולטות כרגע"
    url = news[0]["url"] if news else f"https://www.tradingview.com/symbols/{symbol}"

    message = f"""
<b>{symbol}</b> – ${price:.2f}
📈 המלצה: <b>{decision}</b>
{"💰 מומלץ לקנות בסכום: $" + str(amount) if amount else ""}
📰 חדשות אחרונות: {headline}
🔗 <a href=\"{url}\">קרא עוד</a>
{rec}
📌 נימוקים:
• {'\n• '.join(reasons)}
"""
    return message.strip()

send_telegram("✅ הבוט התחיל לפעול ומוכן לעקוב אחרי המניות שלך \U0001F514")

while True:
    now = datetime.now(us_timezone)
    weekday = now.weekday()  # Monday = 0, Sunday = 6

    if weekday < 5:  # Only update thresholds Monday to Friday
        current_day = now.date()
        if current_day != last_update_day:
            for symbol in stocks:
                try:
                    price = get_price(symbol)
                    new_thresholds = adjust_thresholds(symbol, price)
                    stocks[symbol].update(new_thresholds)
                    print(f"[AUTO-UPDATE] {symbol}: {new_thresholds}")
                except Exception as e:
                    print(f"Error updating {symbol}: {e}")
            last_update_day = current_day

    for symbol, cfg in stocks.items():
        try:
            price = get_price(symbol)
            msg = evaluate(symbol, price, cfg)
            if cfg["last"] != msg:
                send_telegram(msg)
                cfg["last"] = msg
        except Exception as e:
            print(f"{symbol}: {e}")
    time.sleep(300)
