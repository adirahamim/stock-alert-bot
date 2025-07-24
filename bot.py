import requests
import time
import datetime
import pytz
import csv
import matplotlib.pyplot as plt
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TWELVE_API = os.getenv("TWELVE_DATA_API_KEY")
FINNHUB_API = os.getenv("FINNHUB_API_KEY")

# תקציב כולל וניהול הקצאות
TOTAL_BUDGET = 50000
ALLOCATED = {}

# מניות למעקב – ניתן לעדכן ולהוסיף
stocks = {
    "BBAI": {"low": 7.18, "high": 7.80, "buy_price": 7.20, "last": None, "prices": []},
    "SOUN": {"low": 11.40, "high": 12.00, "buy_price": 11.60, "last": None, "prices": []},
    "QS": {"low": 12.00, "high": 13.00, "buy_price": 12.10, "last": None, "prices": []},
    "REKR": {"low": 1.30, "high": 1.48, "buy_price": 1.35, "last": None, "prices": []},
    "QUIK": {"low": 6.10, "high": 6.35, "buy_price": 6.15, "last": None, "prices": []},
    "GDX": {"low": 52.50, "high": 54.00, "buy_price": 53.00, "last": None, "prices": []}
}

last_summary_time = None

def is_market_open():
    now = datetime.datetime.now(pytz.timezone('America/New_York'))
    return now.weekday() < 5 and datetime.time(9, 30) <= now.time() <= datetime.time(16, 0)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_rating(symbol):
    url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={FINNHUB_API}"
    res = requests.get(url).json()
    return res[0] if res else {"buy": 0, "hold": 0, "sell": 0}

def create_graph(symbol, prices):
    if len(prices) < 2:
        return
    plt.figure()
    plt.plot(prices, marker='o')
    plt.title(f"{symbol} – Last Prices")
    plt.axhline(y=stocks[symbol]["low"], color='green', linestyle='--', label='Support')
    plt.axhline(y=stocks[symbol]["high"], color='red', linestyle='--', label='Resistance')
    plt.legend()
    plt.savefig(f"{symbol}.png")
    plt.close()

def get_price(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_API}"
    res = requests.get(url).json()
    return float(res["price"]) if "price" in res else None

def decide_action(symbol, price, rating):
    recommendation = ""
    available = TOTAL_BUDGET - sum(ALLOCATED.values())
    amount_to_buy = min(available, 1000)  # החזקה אגרסיבית

    if price <= stocks[symbol]["low"]:
        recommendation = f"📉 ירידה לאזור קנייה - שקול לרכוש ב־${amount_to_buy:.0f}"
        ALLOCATED[symbol] = ALLOCATED.get(symbol, 0) + amount_to_buy

    elif price >= stocks[symbol]["high"]:
        recommendation = "📈 פריצה מעל התנגדות - אפשרות לכניסה (לסוחרים אגרסיביים)"

    elif rating.get("buy", 0) >= 7 and rating.get("sell", 0) == 0:
        recommendation = f"✅ המלצת אנליסטים חזקה – {rating['buy']} קנייה, מומלץ לשקול רכישה"

    elif rating.get("sell", 0) >= 4:
        recommendation = "🚨 המלצת מכירה חזקה – שקול לצאת מהפוזיציה"

    return recommendation or "🕒 המתנה – אין איתות חזק כרגע"

def run():
    global last_summary_time
    while True:
        if not is_market_open():
            time.sleep(60)
            continue

        for symbol in stocks:
            price = get_price(symbol)
            if not price:
                continue
            stocks[symbol]["last"] = price
            stocks[symbol]["prices"].append(price)
            rating = get_rating(symbol)
            action = decide_action(symbol, price, rating)

            msg = (
                f"📌 {symbol} – ${price:.2f} (ממוצע: ${price:.2f})\n"
                f"אנליסטים 🔍 – קנייה: {rating['buy']} | המתנה: {rating['hold']} | מכירה: {rating['sell']}\n"
                f"{action}"
            )
            send_telegram(msg)
            create_graph(symbol, stocks[symbol]["prices"])
            time.sleep(10)

        now = datetime.datetime.now(pytz.timezone('America/New_York'))
        if not last_summary_time or (now - last_summary_time).seconds > 3600:
            last_summary_time = now
            send_telegram("✅ עדכון בוצע – כל המניות נבדקו שוב")
        time.sleep(60)

if __name__ == "__main__":
    run()
