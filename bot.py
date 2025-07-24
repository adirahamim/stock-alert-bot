import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TWELVE_API = os.getenv("TWELVE_DATA_API_KEY")
FINNHUB_API = os.getenv("FINNHUB_API_KEY")

stocks = {
    "BBAI": {"low": 7.18, "high": 7.80, "buy_price": 7.20, "last": None},
    "QUIK": {"low": 6.10, "high": 6.35, "buy_price": 6.15, "last": None}
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
        return f"🔍 המלצות אנליסטים – קנייה: {rec['buy']} | המתנה: {rec['hold']} | מכירה: {rec['sell']}"
    return "אין המלצות זמינות כרגע"

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
    url = news[0]["url"] if news else "https://www.tradingview.com/symbols/{}".format(symbol)

    message = f"""
<b>{symbol}</b> – ${price:.2f}
📈 המלצה: <b>{decision}</b>
{"💰 מומלץ לקנות בסכום: $" + str(amount) if amount else ""}
📰 חדשות אחרונות: {headline}
🔗 <a href="{url}">קרא עוד</a>
{rec}
📌 נימוקים:
• {'\n• '.join(reasons)}
"""
    return message.strip()

while True:
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
